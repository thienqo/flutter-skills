#!/usr/bin/env python3
"""Run compiler-backed skill evaluations in disposable, constrained fixtures."""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from run_behavior_evals import (
    AgentRunner,
    EvalError,
    git_metadata,
    instructions_for_case,
    load_json,
    skill_catalog,
)


ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE_ROOT = ROOT / ".github" / "evals" / "executable"
CASES_DIR = EXECUTABLE_ROOT / "cases"
FIXTURES_DIR = EXECUTABLE_ROOT / "fixtures"
RUNNER_VERSION = "1.2.0"
ALLOWED_EXECUTABLES = {"dart", "flutter"}
ALLOWED_SUBCOMMANDS = {
    "dart": {"format", "analyze", "test", "run"},
    "flutter": {"analyze", "test", "build"},
}
OFFLINE_FLUTTER_PREPARE = ["flutter", "pub", "get", "--offline", "--enforce-lockfile"]


def relative_path(value: str, identity: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise EvalError(f"{identity} must be a safe relative path")
    return path


def validate_case(case: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    name = case.get("name")
    skill = case.get("skill")
    if not isinstance(name, str) or not name:
        errors.append("executable case requires a name")
    if skill not in catalog:
        errors.append(f"executable case {name}: unknown skill {skill}")
    if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
        errors.append(f"executable case {name}: missing prompt")
    try:
        fixture = relative_path(str(case.get("fixture", "")), "fixture")
        fixture_path = (FIXTURES_DIR / fixture).resolve()
        if not fixture_path.is_relative_to(FIXTURES_DIR.resolve()) or not fixture_path.is_dir():
            errors.append(f"executable case {name}: fixture does not exist")
        elif any(path.is_symlink() for path in fixture_path.rglob("*")):
            errors.append(f"executable case {name}: fixture must not contain symlinks")
    except EvalError as error:
        errors.append(f"executable case {name}: {error}")

    allowed_changes = case.get("allowed_changes")
    if not isinstance(allowed_changes, list) or not allowed_changes:
        errors.append(f"executable case {name}: allowed_changes must be non-empty")
    else:
        for value in allowed_changes:
            if not isinstance(value, str):
                errors.append(f"executable case {name}: allowed changes must be strings")
                continue
            try:
                relative_path(value, "allowed change")
            except EvalError as error:
                errors.append(f"executable case {name}: {error}")

    resources = case.get("resources", [])
    available = set(catalog.get(str(skill), {}).get("resources", {}))
    if not isinstance(resources, list) or not all(isinstance(item, str) for item in resources):
        errors.append(f"executable case {name}: resources must be a string list")
    elif set(resources) - available:
        errors.append(
            f"executable case {name}: unknown resources {sorted(set(resources) - available)}"
        )

    available_skills = case.get("available_skills", [])
    if not isinstance(available_skills, list) or not all(
        isinstance(item, str) for item in available_skills
    ):
        errors.append(f"executable case {name}: available_skills must be a string list")
    else:
        if len(set(available_skills)) != len(available_skills):
            errors.append(f"executable case {name}: duplicate available_skills")
        unknown = set(available_skills) - set(catalog)
        if unknown:
            errors.append(f"executable case {name}: unknown available_skills {sorted(unknown)}")
        if skill in available_skills:
            errors.append(f"executable case {name}: primary skill is already injected")

    checks = case.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append(f"executable case {name}: checks must be non-empty")
    else:
        for index, check in enumerate(checks):
            command = check.get("command") if isinstance(check, dict) else None
            timeout = check.get("timeout", 120) if isinstance(check, dict) else None
            if (
                not isinstance(command, list)
                or not command
                or not all(isinstance(part, str) and part for part in command)
            ):
                errors.append(f"executable case {name}: check {index + 1} has invalid command")
            elif command[0] not in ALLOWED_EXECUTABLES:
                errors.append(
                    f"executable case {name}: check {index + 1} executable is not allowed"
                )
            elif len(command) < 2 or (
                command[1] not in ALLOWED_SUBCOMMANDS[command[0]]
                and command != OFFLINE_FLUTTER_PREPARE
            ):
                errors.append(
                    f"executable case {name}: check {index + 1} subcommand is not allowed"
                )
            else:
                for argument in command[2:]:
                    path_value = argument.partition("=")[2] if "=" in argument else argument
                    candidate = Path(path_value)
                    if candidate.is_absolute() or ".." in candidate.parts:
                        errors.append(
                            f"executable case {name}: check {index + 1} "
                            "must not reference paths outside the fixture"
                        )
                        break
            if not isinstance(timeout, (int, float)) or not 0 < timeout <= 600:
                errors.append(f"executable case {name}: check {index + 1} timeout is invalid")
    return errors


def snapshot(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise EvalError("workspace contains a symlink")
        relative = path.relative_to(root)
        if relative.parts[0] in {".dart_tool", "build"}:
            continue
        if path.is_file() and path.name != ".eval-response.txt":
            files[relative.as_posix()] = path.read_bytes()
    return files


def changed_paths(before: dict[str, bytes], after: dict[str, bytes]) -> list[str]:
    return sorted(
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    )


def path_is_allowed(path: str, allowed_changes: list[str]) -> bool:
    candidate = Path(path)
    return any(
        candidate == allowed or candidate.is_relative_to(allowed)
        for allowed in (Path(value) for value in allowed_changes)
    )


def unified_patch(before: dict[str, bytes], after: dict[str, bytes]) -> str:
    chunks: list[str] = []
    for path in changed_paths(before, after):
        old = before.get(path, b"").decode("utf-8", errors="replace").splitlines(True)
        new = after.get(path, b"").decode("utf-8", errors="replace").splitlines(True)
        chunks.extend(
            difflib.unified_diff(old, new, fromfile=f"a/{path}", tofile=f"b/{path}")
        )
    return "".join(chunks)


def build_prompt(case: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> str:
    instruction_case = {
        "skill": case["skill"],
        "resources": case.get("resources", []),
    }
    allowed = ", ".join(case["allowed_changes"])
    discovery = (
        "Available specialist names, descriptions, and local paths are listed in "
        ".eval-skills/catalog.md. Select and read only the specialists relevant to "
        "this task; do not modify the skill library. State which specialists you "
        "actually read and their implementation or verification ownership.\n\n"
        if case.get("available_skills")
        else ""
    )
    return (
        "Implement the task in the provided disposable fixture. Work only inside "
        f"these allowed paths: {allowed}. Do not edit verification files, package "
        "metadata, or generated configuration. Do not access the network or external "
        "services. Keep the smallest clean change and finish with a concise summary.\n\n"
        f"{discovery}"
        "Apply this skill guidance:\n\n"
        f"<skill>\n{instructions_for_case(instruction_case, catalog)}\n</skill>\n\n"
        f"<task>\n{case['prompt']}\n</task>"
    )


def stage_skill_library(
    workspace: Path, case: dict[str, Any], catalog: dict[str, dict[str, Any]]
) -> None:
    """Expose optional specialists for selective reading, protected by the snapshot."""
    names = case.get("available_skills", [])
    if not names:
        return
    library = workspace / ".eval-skills"
    library.mkdir()
    entries: list[str] = []
    for name in names:
        details = catalog[name]
        directory = library / name
        directory.mkdir()
        (directory / "SKILL.md").write_text(details["instructions"], encoding="utf-8")
        for relative, contents in details.get("resources", {}).items():
            path = directory / relative_path(relative, "skill resource")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        entries.append(f"- {name}: {details['description']} — {name}/SKILL.md")
    (library / "catalog.md").write_text("\n".join(entries) + "\n", encoding="utf-8")


def run_checks(workspace: Path, checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for check in checks:
        command = check["command"]
        try:
            completed = subprocess.run(
                command,
                cwd=workspace,
                text=True,
                capture_output=True,
                check=False,
                timeout=float(check.get("timeout", 120)),
            )
            result = {
                "name": check.get("name") or command[0],
                "command": command,
                "exit_code": completed.returncode,
                "stdout": completed.stdout[-12000:],
                "stderr": completed.stderr[-12000:],
                "passed": completed.returncode == 0,
            }
        except subprocess.TimeoutExpired as error:
            result = {
                "name": check.get("name") or command[0],
                "command": command,
                "exit_code": None,
                "stdout": (error.stdout or "")[-12000:],
                "stderr": (error.stderr or "")[-12000:],
                "passed": False,
                "timed_out": True,
            }
        results.append(result)
        if not result["passed"]:
            break
    return results


def execute_case(
    case: dict[str, Any],
    catalog: dict[str, dict[str, Any]],
    agent: AgentRunner,
) -> dict[str, Any]:
    fixture = FIXTURES_DIR / case["fixture"]
    with tempfile.TemporaryDirectory(prefix="flutter-executable-eval-") as directory:
        baseline_workspace = Path(directory) / "baseline"
        shutil.copytree(fixture, baseline_workspace)
        baseline_checks = run_checks(baseline_workspace, case["checks"])
        if baseline_checks and all(check["passed"] for check in baseline_checks):
            raise EvalError(
                f"executable case {case['name']}: fixture already passes every check"
            )

        workspace = Path(directory) / "candidate"
        shutil.copytree(fixture, workspace)
        stage_skill_library(workspace, case, catalog)
        before = snapshot(workspace)
        response = agent.run_in_workspace(build_prompt(case, catalog), workspace)
        after = snapshot(workspace)
        changes = changed_paths(before, after)
        forbidden = [
            path
            for path in changes
            if not path_is_allowed(path, case["allowed_changes"])
        ]
        checks = [] if forbidden or not changes else run_checks(workspace, case["checks"])
        passed = bool(changes) and not forbidden and bool(checks) and all(
            check["passed"] for check in checks
        )
        return {
            "name": case["name"],
            "skill": case["skill"],
            "available_skills": case.get("available_skills", []),
            "input_sha256": {
                path: hashlib.sha256(contents).hexdigest()
                for path, contents in before.items()
            },
            "prompt": build_prompt(case, catalog),
            "agent_response": response,
            "changed_paths": changes,
            "forbidden_changes": forbidden,
            "patch": unified_patch(before, after),
            "baseline_checks": baseline_checks,
            "checks": checks,
            "passed": passed,
        }


def discover_cases() -> list[tuple[Path, dict[str, Any]]]:
    return [(path, load_json(path)) for path in sorted(CASES_DIR.glob("*.json"))]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--agent", choices=("codex",), default="codex")
    parser.add_argument("--model")
    parser.add_argument("--agent-timeout", type=float, default=300)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = skill_catalog()
    discovered = discover_cases()
    errors = [
        f"{path}: {error}"
        for path, case in discovered
        for error in validate_case(case, catalog)
    ]
    if not discovered:
        errors.append("no executable cases found")
    if errors:
        raise EvalError("; ".join(errors))
    selected = [
        case for _, case in discovered if args.case is None or case["name"] == args.case
    ]
    if not selected:
        raise EvalError("no executable case matched --case")
    print(f"Validated {len(discovered)} executable eval cases.")
    if not args.execute:
        print("Validation-only mode; pass --execute to invoke an agent and checks.")
        return 0

    agent = AgentRunner(args.agent, args.model, args.agent_timeout)
    case_results = [execute_case(case, catalog, agent) for case in selected]
    result = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "runner_version": RUNNER_VERSION,
        "git": git_metadata(),
        "agent": args.agent,
        "agent_version": agent.version(),
        "model": args.model,
        "cases": case_results,
        "summary": {
            "cases": len(case_results),
            "passed": sum(case["passed"] for case in case_results),
        },
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote results to {args.output}")
    for case in case_results:
        print(f"executable {case['skill']}:{case['name']} passed={case['passed']}")
    return 0 if all(case["passed"] for case in case_results) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvalError as error:
        print(f"ERROR: {error}")
        raise SystemExit(2)
