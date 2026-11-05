#!/usr/bin/env python3
"""Run or validate forward evaluations for the Flutter skill catalog.

Validation is local and deterministic. Executing an eval deliberately invokes an
external coding agent and can incur cost, so it requires --execute and defaults
to one case. Use --all-cases only for an intentional collection-wide run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
ROUTING_CASES_PATH = ROOT / ".github" / "evals" / "routing-cases.json"
DEFAULT_PROFILE_PATH = ROOT / ".github" / "evals" / "public-benchmark.json"
PROFILES_DIR = ROOT / ".github" / "evals" / "profiles"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_REFERENCE_PATTERN = re.compile(r"\[[^\]]+\]\((references/[^)#]+\.md)(?:#[^)]+)?\)")
RUNNER_VERSION = "2.0.0"


def expectation_text(item: str | dict[str, Any]) -> str:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        return str(item.get("text", "")).strip()
    return ""


def is_mandatory_expectation(item: str | dict[str, Any]) -> bool:
    if isinstance(item, dict):
        return bool(item.get("mandatory", False))
    return False


def git_metadata() -> dict[str, Any]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        dirty = bool(status)
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        return {
            "commit": commit or None,
            "dirty": dirty,
            "branch": branch or None,
        }
    except Exception:
        return {"commit": None, "dirty": None, "branch": None}



class EvalError(RuntimeError):
    """Raised when eval configuration or agent output is invalid."""


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def skill_catalog() -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        try:
            frontmatter, _ = text[4:].split("\n---\n", 1)
        except ValueError as error:
            raise EvalError(f"{skill_file}: malformed frontmatter") from error
        metadata: dict[str, str] = {}
        for line in frontmatter.splitlines():
            key, separator, value = line.partition(":")
            if separator and not line.startswith((" ", "\t")):
                metadata[key.strip()] = value.strip().strip('"').strip("'")
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if not name or not description:
            raise EvalError(f"{skill_file}: missing name or description")
        resources: dict[str, str] = {}
        for relative_path in LOCAL_REFERENCE_PATTERN.findall(text):
            reference_path = skill_file.parent / relative_path
            if not reference_path.is_file():
                raise EvalError(f"{skill_file}: missing reference {relative_path}")
            resources[relative_path] = reference_path.read_text(encoding="utf-8")
        catalog[name] = {
            "description": description,
            "instructions": text,
            "resources": resources,
        }
    return catalog


def behavior_cases(catalog: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for skill_name in sorted(catalog):
        path = ROOT / ".github" / "evals" / "behavior" / skill_name / "cases.json"
        for case in load_json(path):
            cases.append({**case, "skill": skill_name})
    return cases


def routing_cases() -> list[dict[str, Any]]:
    return load_json(ROUTING_CASES_PATH)


def validate_benchmark_profile(
    profile: dict[str, Any],
    behavior: Iterable[dict[str, Any]],
    routing: Iterable[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(profile.get("name"), str) or not profile["name"].strip():
        errors.append("benchmark profile requires a name")
    behavior_ids = {(case["skill"], case["name"]) for case in behavior}
    requested_behavior = profile.get("behavior")
    if requested_behavior == "all":
        pass
    elif not isinstance(requested_behavior, list) or not requested_behavior:
        errors.append("benchmark profile requires behavior cases")
    else:
        seen_behavior: set[tuple[str, str]] = set()
        for index, item in enumerate(requested_behavior):
            if not isinstance(item, dict):
                errors.append(f"benchmark behavior item {index + 1} must be an object")
                continue
            identity = (item.get("skill"), item.get("case"))
            if not all(isinstance(value, str) for value in identity):
                errors.append(f"benchmark behavior item {index + 1} is invalid")
            elif identity not in behavior_ids:
                errors.append(f"benchmark profile has unknown behavior case {identity[0]}:{identity[1]}")
            elif identity in seen_behavior:
                errors.append(f"benchmark profile repeats behavior case {identity[0]}:{identity[1]}")
            else:
                seen_behavior.add(identity)

    routing_names = {case["name"] for case in routing}
    requested_routing = profile.get("routing")
    if requested_routing == "all":
        pass
    elif not isinstance(requested_routing, list) or not requested_routing:
        errors.append("benchmark profile requires routing cases")
    elif not all(isinstance(name, str) for name in requested_routing):
        errors.append("benchmark routing cases must be strings")
    else:
        unknown = set(requested_routing) - routing_names
        if unknown:
            errors.append(f"benchmark profile has unknown routing cases {sorted(unknown)}")
        if len(requested_routing) != len(set(requested_routing)):
            errors.append("benchmark profile repeats a routing case")
    return errors


def cases_for_profile(
    profile: dict[str, Any],
    behavior: list[dict[str, Any]],
    routing: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    behavior_by_id = {(case["skill"], case["name"]): case for case in behavior}
    routing_by_name = {case["name"]: case for case in routing}
    selected_behavior = (
        behavior
        if profile["behavior"] == "all"
        else [
            behavior_by_id[(item["skill"], item["case"])]
            for item in profile["behavior"]
        ]
    )
    selected_routing = (
        routing
        if profile["routing"] == "all"
        else [routing_by_name[name] for name in profile["routing"]]
    )
    return selected_behavior, selected_routing


def validate_behavior_cases(
    cases: Iterable[dict[str, Any]],
    catalog: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for case in cases:
        identity = f"{case.get('skill', '')}:{case.get('name', '')}"
        if identity in seen:
            errors.append(f"duplicate behavior case {identity}")
        seen.add(identity)
        if not NAME_PATTERN.fullmatch(str(case.get("name", ""))):
            errors.append(f"{identity}: invalid name")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{identity}: missing prompt")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or not expectations:
            errors.append(f"{identity}: missing expectations")
        else:
            for index, item in enumerate(expectations):
                if isinstance(item, str):
                    if not item.strip():
                        errors.append(f"{identity}: expectation {index + 1} must not be empty")
                elif isinstance(item, dict):
                    text = item.get("text")
                    if not isinstance(text, str) or not text.strip():
                        errors.append(f"{identity}: expectation {index + 1} must have a non-empty text")
                    if "mandatory" in item and not isinstance(item["mandatory"], bool):
                        errors.append(f"{identity}: expectation {index + 1} mandatory must be boolean")
                    if "id" in item and (not isinstance(item["id"], str) or not item["id"].strip()):
                        errors.append(f"{identity}: expectation {index + 1} id must be a non-empty string")
                    unknown_keys = set(item) - {"text", "id", "mandatory"}
                    if unknown_keys:
                        errors.append(f"{identity}: expectation {index + 1} has unknown keys {sorted(unknown_keys)}")
                else:
                    errors.append(f"{identity}: expectation {index + 1} must be a string or object")
        resources = case.get("resources", [])
        if not isinstance(resources, list) or not all(
            isinstance(item, str) and item.strip() for item in resources
        ):
            errors.append(f"{identity}: resources must be a string list")
        elif len(resources) != len(set(resources)):
            errors.append(f"{identity}: resources must not contain duplicates")
        elif catalog is not None:
            skill_name = str(case.get("skill", ""))
            available = set(catalog.get(skill_name, {}).get("resources", {}))
            unknown = set(resources) - available
            if unknown:
                errors.append(f"{identity}: unknown resources {sorted(unknown)}")
    return errors


def instructions_for_case(
    case: dict[str, Any], catalog: dict[str, dict[str, Any]]
) -> str:
    details = catalog[case["skill"]]
    instructions = str(details["instructions"])
    selected_resources = case.get("resources", [])
    if not selected_resources:
        return instructions

    resources = details["resources"]
    blocks = [
        f"<resource path=\"{relative_path}\">\n"
        f"{resources[relative_path]}\n"
        "</resource>"
        for relative_path in selected_resources
    ]
    return (
        instructions
        + "\n\n<supporting_resources>\n"
        + "\n\n".join(blocks)
        + "\n</supporting_resources>"
    )


def validate_routing_cases(
    cases: Iterable[dict[str, Any]], catalog_names: set[str]
) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for case in cases:
        name = case.get("name", "")
        if name in seen:
            errors.append(f"duplicate routing case {name}")
        seen.add(name)
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            errors.append(f"routing case {name!r}: invalid name")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"routing case {name}: missing prompt")
        groups: dict[str, set[str]] = {}
        for field in ("required", "optional", "forbidden"):
            values = case.get(field)
            if not isinstance(values, list) or not all(
                isinstance(value, str) for value in values
            ):
                errors.append(f"routing case {name}: {field} must be a string list")
                groups[field] = set()
                continue
            groups[field] = set(values)
            unknown = groups[field] - catalog_names
            if unknown:
                errors.append(
                    f"routing case {name}: {field} has unknown skills {sorted(unknown)}"
                )
        if not groups.get("required"):
            errors.append(f"routing case {name}: requires at least one skill")
        fields = ("required", "optional", "forbidden")
        for index, left in enumerate(fields):
            for right in fields[index + 1 :]:
                overlap = groups.get(left, set()) & groups.get(right, set())
                if overlap:
                    errors.append(
                        f"routing case {name}: {left}/{right} overlap {sorted(overlap)}"
                    )
    return errors


def build_behavior_prompt(
    case: dict[str, Any], instructions: str | None
) -> str:
    context = (
        "No skill is injected. Solve the user request using your normal judgment."
        if instructions is None
        else "Apply the following skill faithfully while preserving the user's scope:\n\n"
        f"<skill>\n{instructions}\n</skill>"
    )
    return (
        "You are completing a forward evaluation. Do not mention the evaluation, "
        "rubric, or injected context. Return the response you would give the user. "
        "Do not access files, tools, or external services; reason from the request "
        "and supplied context only.\n\n"
        f"{context}\n\n<user_request>\n{case['prompt']}\n</user_request>"
    )


def build_judge_prompt(case: dict[str, Any], response: str) -> str:
    criteria = "\n".join(
        f"{index + 1}. {'[MANDATORY] ' if is_mandatory_expectation(expectation) else ''}{expectation_text(expectation)}"
        for index, expectation in enumerate(case["expectations"])
    )
    return (
        "Judge the candidate response only against the supplied criteria. Treat a "
        "criterion as met only when the response makes the required decision or "
        "verification explicit. Do not reward matching phrases without the behavior. "
        "Return only JSON with keys score (integer 0-100), expectations (an array of "
        "objects with criterion, met, and evidence), and summary.\n\n"
        f"<task>\n{case['prompt']}\n</task>\n\n"
        f"<criteria>\n{criteria}\n</criteria>\n\n"
        f"<candidate_response>\n{response}\n</candidate_response>"
    )


def build_routing_prompt(
    case: dict[str, Any], catalog: dict[str, dict[str, Any]]
) -> str:
    entries = "\n".join(
        f"- {name}: {details['description']}" for name, details in sorted(catalog.items())
    )
    return (
        "Select the smallest set of skills needed for the user request. Choose only "
        "from the catalog. Include a workflow skill only for end-to-end delivery "
        "coordinating UI, state or business logic, data, tests, and runtime verification. "
        "Multiple files or two technical domains alone do not require a workflow; use "
        "specialists directly for contained work. Data-only synchronization and a "
        "single screen or form remain specialist tasks. Generic verification does not "
        "require device testing unless a concrete runtime target must be operated. "
        "Return only JSON with keys "
        "skills (an array of names) and reason (one short string).\n\n"
        f"<catalog>\n{entries}\n</catalog>\n\n"
        f"<user_request>\n{case['prompt']}\n</user_request>"
    )


def extract_json_object(text: str) -> dict[str, Any]:
    candidates = [text.strip()]
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        candidates.insert(0, fenced.group(1))
    first = text.find("{")
    last = text.rfind("}")
    if first >= 0 and last > first:
        candidates.append(text[first : last + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise EvalError("agent did not return a JSON object")


def score_routing_selection(
    case: dict[str, Any], selected: Iterable[str]
) -> dict[str, Any]:
    selected_set = set(selected)
    required = set(case["required"])
    optional = set(case["optional"])
    forbidden = set(case["forbidden"])
    missing = required - selected_set
    forbidden_selected = forbidden & selected_set
    unexpected = selected_set - required - optional
    passed = not missing and not forbidden_selected and not unexpected
    return {
        "passed": passed,
        "selected": sorted(selected_set),
        "missing": sorted(missing),
        "forbidden_selected": sorted(forbidden_selected),
        "unexpected": sorted(unexpected),
    }


def validate_judgment(
    judgment: dict[str, Any], expected_count: int, identity: str
) -> None:
    score = judgment.get("score")
    if not isinstance(score, int) or not 0 <= score <= 100:
        raise EvalError(f"{identity}: judge score must be an integer from 0 to 100")
    expectations = judgment.get("expectations")
    if not isinstance(expectations, list) or len(expectations) != expected_count:
        raise EvalError(
            f"{identity}: judge returned {len(expectations) if isinstance(expectations, list) else 'invalid'} "
            f"expectations; expected {expected_count}"
        )
    for index, item in enumerate(expectations):
        if not isinstance(item, dict) or not isinstance(item.get("met"), bool):
            raise EvalError(f"{identity}: judgment expectation {index + 1} is invalid")
        if not isinstance(item.get("criterion"), str) or not isinstance(
            item.get("evidence"), str
        ):
            raise EvalError(f"{identity}: judgment expectation {index + 1} lacks evidence")


def aggregate_judgments(
    judgments: list[dict[str, Any]],
    expectations: list[str | dict[str, Any]],
) -> dict[str, Any]:
    if not judgments:
        raise EvalError("at least one judgment is required")

    scores = [int(judgment["score"]) for judgment in judgments]
    unanimous_expectations = 0
    mandatory_disagreements: list[str] = []
    for index, expectation in enumerate(expectations):
        decisions = {
            bool(judgment["expectations"][index]["met"])
            for judgment in judgments
        }
        if len(decisions) == 1:
            unanimous_expectations += 1
        elif is_mandatory_expectation(expectation):
            identifier = (
                expectation.get("id", f"expectation-{index + 1}")
                if isinstance(expectation, dict)
                else f"expectation-{index + 1}"
            )
            mandatory_disagreements.append(str(identifier))

    expectation_count = len(expectations)
    return {
        "judge_count": len(judgments),
        "average_score": round(sum(scores) / len(scores), 2),
        "minimum_score": min(scores),
        "maximum_score": max(scores),
        "score_range": max(scores) - min(scores),
        "expectation_count": expectation_count,
        "unanimous_expectations": unanimous_expectations,
        "expectation_agreement_rate": round(
            unanimous_expectations / expectation_count * 100, 2
        ),
        "mandatory_disagreements": mandatory_disagreements,
    }


def run_judgments(
    judges: list["AgentRunner"],
    prompt: str,
    expectations: list[str | dict[str, Any]],
    identity: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    judgments: list[dict[str, Any]] = []
    for index, judge in enumerate(judges):
        judgment = extract_json_object(judge.run(prompt))
        validate_judgment(
            judgment,
            len(expectations),
            f"{identity}:judge-{index + 1}",
        )
        judgments.append(judgment)
    return judgments, aggregate_judgments(judgments, expectations)


def judgment_block(
    response: str,
    judgments: list[dict[str, Any]],
    agreement: dict[str, Any],
) -> dict[str, Any]:
    return {
        "response": response,
        # Keep the first judgment for compatibility with existing raw results.
        "judgment": judgments[0],
        "judgments": judgments,
        "agreement": agreement,
    }


class AgentRunner:
    def __init__(
        self, agent: str, model: str | None, timeout_seconds: float = 180.0
    ) -> None:
        self.agent = agent
        self.model = model
        self.timeout_seconds = timeout_seconds
        executable = shutil.which(agent)
        if executable is None:
            raise EvalError(f"required agent executable not found: {agent}")
        self.executable = executable

    def version(self) -> str:
        completed = subprocess.run(
            [self.executable, "--version"],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise EvalError(detail or f"unable to read {self.agent} version")
        return completed.stdout.strip()

    def run(self, prompt: str) -> str:
        if self.agent == "claude":
            command = [
                self.executable,
                "-p",
                "--safe-mode",
                "--no-session-persistence",
                "--tools",
                "",
                "--output-format",
                "text",
            ]
            if self.model:
                command.extend(["--model", self.model])
            try:
                completed = subprocess.run(
                    command,
                    input=prompt,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=self.timeout_seconds,
                )
            except subprocess.TimeoutExpired as error:
                raise EvalError(
                    f"{self.agent} eval timed out after "
                    f"{self.timeout_seconds:g} seconds"
                ) from error
            if completed.returncode:
                detail = completed.stderr.strip() or completed.stdout.strip()
                raise EvalError(detail or "claude eval failed")
            return completed.stdout.strip()

        with tempfile.TemporaryDirectory(prefix="flutter-skill-eval-") as directory:
            result_path = Path(directory) / "response.txt"
            command = [
                self.executable,
                "exec",
                "--ephemeral",
                "--skip-git-repo-check",
                "--ignore-user-config",
                "--ignore-rules",
                "--sandbox",
                "read-only",
                "--cd",
                directory,
                "--output-last-message",
                str(result_path),
            ]
            if self.model:
                command.extend(["--model", self.model])
            command.append("-")
            try:
                completed = subprocess.run(
                    command,
                    input=prompt,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=self.timeout_seconds,
                )
            except subprocess.TimeoutExpired as error:
                raise EvalError(
                    f"{self.agent} eval timed out after "
                    f"{self.timeout_seconds:g} seconds"
                ) from error
            if completed.returncode:
                detail = completed.stderr.strip() or completed.stdout.strip()
                raise EvalError(detail or "codex eval failed")
            if not result_path.is_file():
                raise EvalError("codex did not write a final response")
            return result_path.read_text(encoding="utf-8").strip()

    def run_in_workspace(self, prompt: str, workspace: Path) -> str:
        if self.agent != "codex":
            raise EvalError(
                "executable workspace evals currently support codex only; "
                "add another CLI only after its non-interactive write and sandbox "
                "contract is verified"
            )
        result_path = workspace / ".eval-response.txt"
        command = [
            self.executable,
            "exec",
            "--ephemeral",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "workspace-write",
            "--cd",
            str(workspace),
            "--output-last-message",
            str(result_path),
        ]
        if self.model:
            command.extend(["--model", self.model])
        command.append("-")
        try:
            completed = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            raise EvalError(
                f"{self.agent} executable eval timed out after "
                f"{self.timeout_seconds:g} seconds"
            ) from error
        if completed.returncode:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise EvalError(detail or "codex executable eval failed")
        if not result_path.is_file():
            raise EvalError("codex did not write a final executable-eval response")
        response = result_path.read_text(encoding="utf-8").strip()
        result_path.unlink()
        return response


def select_cases(
    cases: list[dict[str, Any]], args: argparse.Namespace
) -> list[dict[str, Any]]:
    selected = cases
    if args.skill:
        wanted = set(args.skill)
        selected = [case for case in selected if case.get("skill") in wanted]
    if args.case:
        pattern = re.compile(args.case)
        selected = [case for case in selected if pattern.search(case["name"])]
    if not args.all_cases:
        selected = selected[: args.max_cases]
    return selected


def run_behavior_suite(
    cases: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    solver: AgentRunner,
    judges: list[AgentRunner],
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for case in cases:
        result: dict[str, Any] = {"skill": case["skill"], "case": case["name"]}
        if not args.skip_baseline:
            baseline_response = solver.run(build_behavior_prompt(case, None))
            baseline_judgments, baseline_agreement = run_judgments(
                judges,
                build_judge_prompt(case, baseline_response),
                case["expectations"],
                f"{case['skill']}:{case['name']}:baseline",
            )
            result["baseline"] = judgment_block(
                baseline_response,
                baseline_judgments,
                baseline_agreement,
            )
        skill_response = solver.run(
            build_behavior_prompt(case, instructions_for_case(case, catalog))
        )
        skill_judgments, skill_agreement = run_judgments(
            judges,
            build_judge_prompt(case, skill_response),
            case["expectations"],
            f"{case['skill']}:{case['name']}:with-skill",
        )
        result["with_skill"] = judgment_block(
            skill_response,
            skill_judgments,
            skill_agreement,
        )
        baseline_score = result.get("baseline", {}).get("agreement", {}).get(
            "average_score"
        )
        skill_score = skill_agreement["average_score"]
        result["delta"] = (
            skill_score - baseline_score
            if isinstance(skill_score, (int, float))
            and isinstance(baseline_score, (int, float))
            else None
        )
        mandatory_failure = any(
            not judgment["expectations"][index]["met"]
            for judgment in skill_judgments
            for index, expectation in enumerate(case["expectations"])
            if is_mandatory_expectation(expectation)
        )
        result["mandatory_failure"] = mandatory_failure
        result["passed"] = (
            all(judgment["score"] >= args.threshold for judgment in skill_judgments)
            and not mandatory_failure
        )
        results.append(result)
        print(
            f"behavior {case['skill']}:{case['name']} "
            f"score={skill_score} judges={len(judges)} "
            f"agreement={skill_agreement['expectation_agreement_rate']}% "
            f"delta={result['delta']} "
            f"mandatory_failure={mandatory_failure} passed={result['passed']}",
            flush=True,
        )
    return results


def run_routing_suite(
    cases: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    solver: AgentRunner,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for case in cases:
        response = solver.run(build_routing_prompt(case, catalog))
        parsed = extract_json_object(response)
        selected = parsed.get("skills")
        if not isinstance(selected, list) or not all(
            isinstance(item, str) for item in selected
        ):
            raise EvalError(f"routing case {case['name']}: invalid skills output")
        score = score_routing_selection(case, selected)
        result = {
            "case": case["name"],
            "response": parsed,
            **score,
        }
        results.append(result)
        print(
            f"routing {case['name']} selected={score['selected']} "
            f"passed={score['passed']}",
            flush=True,
        )
    return results


def result_summary(results: dict[str, Any]) -> dict[str, Any]:
    behavior = results["behavior"]
    routing = results["routing"]
    def block_score(block: dict[str, Any]) -> float:
        return float(
            block.get("agreement", {}).get(
                "average_score", block["judgment"]["score"]
            )
        )

    baseline_scores = [block_score(item["baseline"]) for item in behavior if "baseline" in item]
    skill_scores = [block_score(item["with_skill"]) for item in behavior]
    multi_judge_blocks = [
        item[phase]
        for item in behavior
        for phase in ("baseline", "with_skill")
        if phase in item and item[phase].get("agreement", {}).get("judge_count", 1) > 1
    ]

    def average(values: list[float]) -> float | None:
        return round(sum(values) / len(values), 2) if values else None

    total_expectations = sum(
        block["agreement"]["expectation_count"] for block in multi_judge_blocks
    )
    total_unanimous = sum(
        block["agreement"]["unanimous_expectations"] for block in multi_judge_blocks
    )
    by_skill_values: dict[str, dict[str, Any]] = {}
    for item in behavior:
        values = by_skill_values.setdefault(
            item["skill"],
            {"cases": 0, "passed": 0, "baseline": [], "with_skill": []},
        )
        values["cases"] += 1
        values["passed"] += int(bool(item["passed"]))
        if "baseline" in item:
            values["baseline"].append(block_score(item["baseline"]))
        values["with_skill"].append(block_score(item["with_skill"]))
    by_skill = {
        skill: {
            "cases": values["cases"],
            "passed": values["passed"],
            "baseline_average": average(values["baseline"]),
            "with_skill_average": average(values["with_skill"]),
            "average_delta": (
                round(
                    average(values["with_skill"]) - average(values["baseline"]), 2
                )
                if values["baseline"]
                else None
            ),
        }
        for skill, values in sorted(by_skill_values.items())
    }

    return {
        "behavior_cases": len(behavior),
        "behavior_passed": sum(bool(item["passed"]) for item in behavior),
        "mandatory_failures": sum(bool(item.get("mandatory_failure")) for item in behavior),
        "baseline_average": average(baseline_scores),
        "with_skill_average": average(skill_scores),
        "average_delta": (
            round(average(skill_scores) - average(baseline_scores), 2)
            if skill_scores and baseline_scores
            else None
        ),
        "judge_agreement_rate": (
            round(total_unanimous / total_expectations * 100, 2)
            if total_expectations
            else None
        ),
        "judge_score_range_average": average(
            [float(block["agreement"]["score_range"]) for block in multi_judge_blocks]
        ),
        "mandatory_judge_disagreements": sum(
            len(block["agreement"]["mandatory_disagreements"])
            for block in multi_judge_blocks
        ),
        "by_skill": by_skill,
        "routing_cases": len(routing),
        "routing_passed": sum(bool(item["passed"]) for item in routing),
    }


def markdown_report(results: dict[str, Any]) -> str:
    summary = results["summary"]

    def display(value: Any) -> str:
        return "—" if value is None else str(value)

    judges = results.get("judges") or [
        {
            "agent": results.get("judge_agent"),
            "model": results.get("judge_model"),
        }
    ]
    judge_names = ", ".join(
        f"{judge.get('agent')}" + (f"/{judge['model']}" if judge.get("model") else "")
        for judge in judges
    )
    lines = [
        f"# {results.get('profile', {}).get('name', 'Focused evaluation') if results.get('profile') else 'Focused evaluation'}",
        "",
        f"- Solver: `{results.get('agent')}`",
        f"- Judges: `{judge_names}`",
        f"- Independent primary judge: {'yes' if results.get('independent_primary_judge') else 'no'}",
        f"- Behavior: {summary['behavior_passed']}/{summary['behavior_cases']} passed",
        f"- Routing: {summary['routing_passed']}/{summary['routing_cases']} passed",
        f"- Judge agreement: {display(summary.get('judge_agreement_rate'))}%",
        "",
        "| Skill | Cases | Passed | Baseline | With skill | Delta |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for skill, values in summary.get("by_skill", {}).items():
        lines.append(
            f"| `{skill}` | {values['cases']} | {values['passed']} | "
            f"{display(values['baseline_average'])} | "
            f"{display(values['with_skill_average'])} | "
            f"{display(values['average_delta'])} |"
        )
    lines.extend(
        [
            "",
            "This table is a summary. Retain the source JSON for responses, individual judgments, disagreements, and failed cases.",
            "",
        ]
    )
    return "\n".join(lines)


def reference_coverage_report(
    catalog: dict[str, dict[str, Any]], cases: list[dict[str, Any]]
) -> dict[str, Any]:
    used_resources_by_skill: dict[str, set[str]] = {skill: set() for skill in catalog}
    for case in cases:
        skill = case.get("skill", "")
        if skill in used_resources_by_skill:
            for resource in case.get("resources", []):
                used_resources_by_skill[skill].add(resource)

    total_refs = 0
    total_covered = 0
    by_skill: dict[str, dict[str, Any]] = {}

    for skill_name, details in sorted(catalog.items()):
        available = set(details.get("resources", {}))
        covered = available & used_resources_by_skill.get(skill_name, set())
        uncovered = available - covered
        total_refs += len(available)
        total_covered += len(covered)
        rate = round(len(covered) / len(available) * 100, 1) if available else 100.0
        by_skill[skill_name] = {
            "total": len(available),
            "covered": len(covered),
            "uncovered": sorted(uncovered),
            "coverage_rate": rate,
        }

    overall_rate = round(total_covered / total_refs * 100, 1) if total_refs else 100.0
    return {
        "total_references": total_refs,
        "covered_references": total_covered,
        "uncovered_references": total_refs - total_covered,
        "coverage_rate": overall_rate,
        "by_skill": by_skill,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="invoke external agents")
    parser.add_argument(
        "--suite", choices=("all", "behavior", "routing"), default="all"
    )
    parser.add_argument("--agent", choices=("claude", "codex"), default="codex")
    parser.add_argument(
        "--judge-agent",
        action="append",
        choices=("claude", "codex"),
        help="judge CLI; repeat for independent judgments",
    )
    parser.add_argument("--model")
    parser.add_argument(
        "--judge-model",
        action="append",
        help="judge model in judge order; repeat to match --judge-agent",
    )
    parser.add_argument(
        "--require-independent-judge",
        action="store_true",
        help="fail unless the primary judge CLI differs from the solver CLI",
    )
    parser.add_argument(
        "--agent-timeout",
        type=float,
        default=180.0,
        help="maximum seconds for each solver or judge invocation",
    )
    parser.add_argument("--skill", action="append", help="filter behavior skill")
    parser.add_argument("--case", help="regular expression for case names")
    parser.add_argument("--max-cases", type=int, default=1)
    parser.add_argument(
        "--all-cases", action="store_true", help="explicitly run every matching case"
    )
    parser.add_argument("--skip-baseline", action="store_true")
    parser.add_argument("--threshold", type=int, default=80)
    parser.add_argument(
        "--coverage", action="store_true", help="report reference document evaluation coverage"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument(
        "--profile",
        type=Path,
        help="run the exact behavior and routing cases in a benchmark profile",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_cases < 1:
        raise EvalError("--max-cases must be positive")
    if args.agent_timeout <= 0:
        raise EvalError("--agent-timeout must be positive")
    if not 0 <= args.threshold <= 100:
        raise EvalError("--threshold must be between 0 and 100")
    requested_judges = args.judge_agent or [args.agent]
    requested_judge_models = args.judge_model or []
    if len(requested_judge_models) > len(requested_judges):
        raise EvalError("--judge-model cannot outnumber --judge-agent")
    if args.judge_model and not args.judge_agent and len(args.judge_model) > 1:
        raise EvalError("multiple --judge-model values require repeated --judge-agent")
    judge_models = requested_judge_models + [None] * (
        len(requested_judges) - len(requested_judge_models)
    )
    if args.require_independent_judge and requested_judges[0] == args.agent:
        raise EvalError("the primary judge must differ from the solver")

    catalog = skill_catalog()
    all_behavior = behavior_cases(catalog)
    all_routing = routing_cases()
    errors = validate_behavior_cases(all_behavior, catalog)
    errors.extend(validate_routing_cases(all_routing, set(catalog)))
    profile_paths = [DEFAULT_PROFILE_PATH, *sorted(PROFILES_DIR.glob("*.json"))]
    seen_profile_names: set[str] = set()
    for profile_path in profile_paths:
        candidate_profile = load_json(profile_path)
        profile_name = candidate_profile.get("name")
        if profile_name in seen_profile_names:
            errors.append(f"{profile_path}: duplicate benchmark profile name {profile_name}")
        elif isinstance(profile_name, str):
            seen_profile_names.add(profile_name)
        errors.extend(
            f"{profile_path}: {error}"
            for error in validate_benchmark_profile(
                candidate_profile, all_behavior, all_routing
            )
        )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(all_behavior)} behavior cases and "
        f"{len(all_routing)} routing cases."
    )
    coverage_data: dict[str, Any] | None = None
    if args.coverage:
        coverage_data = reference_coverage_report(catalog, all_behavior)
        print("Reference Coverage Report:")
        for skill_name, data in coverage_data["by_skill"].items():
            if data["total"] > 0:
                status = f"{data['covered']}/{data['total']} ({data['coverage_rate']}%)"
                uncovered_note = f" - missing: {', '.join(data['uncovered'])}" if data["uncovered"] else ""
                print(f"  {skill_name}: {status}{uncovered_note}")
        print(
            f"Total references: {coverage_data['total_references']}, "
            f"Covered: {coverage_data['covered_references']} ({coverage_data['coverage_rate']}%), "
            f"Uncovered: {coverage_data['uncovered_references']}"
        )
    if not args.execute:
        if args.coverage:
            return 0 if coverage_data and coverage_data["uncovered_references"] == 0 else 1
        print("Validation-only mode; pass --execute to invoke an external agent.")
        return 0

    profile: dict[str, Any] | None = None
    profile_behavior: list[dict[str, Any]] = []
    profile_routing: list[dict[str, Any]] = []
    if args.profile:
        if args.skill or args.case or args.all_cases:
            raise EvalError("--profile cannot be combined with case filters")
        profile = load_json(args.profile)
        profile_errors = validate_benchmark_profile(
            profile, all_behavior, all_routing
        )
        if profile_errors:
            raise EvalError("; ".join(profile_errors))
        profile_behavior, profile_routing = cases_for_profile(
            profile, all_behavior, all_routing
        )

    solver = AgentRunner(args.agent, args.model, args.agent_timeout)
    judges = [
        AgentRunner(agent, model, args.agent_timeout)
        for agent, model in zip(requested_judges, judge_models)
    ]
    judge_metadata = [
        {
            "agent": agent,
            "version": judge.version(),
            "model": model,
        }
        for judge, agent, model in zip(judges, requested_judges, judge_models)
    ]
    results: dict[str, Any] = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "runner_version": RUNNER_VERSION,
        "git": git_metadata(),
        "agent": args.agent,
        "agent_version": solver.version(),
        "model": args.model,
        # Preserve the primary judge fields for existing result consumers.
        "judge_agent": judge_metadata[0]["agent"],
        "judge_agent_version": judge_metadata[0]["version"],
        "judge_model": judge_metadata[0]["model"],
        "judges": judge_metadata,
        "independent_primary_judge": judge_metadata[0]["agent"] != args.agent,
        "catalog_version": load_json(ROOT / "package.json")["version"],
        "profile": profile,
        "reference_coverage": coverage_data if args.coverage else None,
        "behavior": [],
        "routing": [],
    }
    if args.suite in ("all", "behavior"):
        selected_behavior = (
            profile_behavior if profile is not None else select_cases(all_behavior, args)
        )
        if not selected_behavior:
            raise EvalError("no behavior cases matched the requested filters")
        results["behavior"] = run_behavior_suite(
            selected_behavior, catalog, solver, judges, args
        )
    if args.suite in ("all", "routing"):
        if profile is not None:
            selected_routing = profile_routing
        else:
            routing_args = argparse.Namespace(**vars(args))
            routing_args.skill = None
            selected_routing = select_cases(all_routing, routing_args)
        if not selected_routing:
            raise EvalError("no routing cases matched the requested filters")
        results["routing"] = run_routing_suite(selected_routing, catalog, solver)

    results["summary"] = result_summary(results)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote results to {args.output}")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown_report(results), encoding="utf-8")
        print(f"Wrote Markdown report to {args.markdown_output}")

    passed = all(item["passed"] for item in results["behavior"] + results["routing"])
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvalError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
