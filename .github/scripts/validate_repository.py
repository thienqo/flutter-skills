#!/usr/bin/env python3
"""Validate the public Flutter Agent Skills catalog and package metadata."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MAX_DESCRIPTION = 500
MAX_COMBINED_DESCRIPTION = 12_000
IGNORED_LINK_DIRECTORIES = {
    ".agents",
    ".codex",
    ".dart_tool",
    ".eval-results",
    ".git",
    ".tessl",
    "build",
    "coverage",
    "node_modules",
}
EXPECTED_VERSION = "0.10.0"
EXPECTED_SKILL_COUNT = 37
EXPECTED_EVAL_COUNT = 220
EXPECTED_ROUTING_EVAL_COUNT = 76
EXPECTED_BUNDLES = {
    "all-flutter-skills": {
        "dart-concurrency",
        "dart-language",
        "flutter-accessibility",
        "flutter-ai-integration",
        "flutter-animation",
        "flutter-app-workflow",
        "flutter-architecture",
        "flutter-authentication",
        "flutter-background-execution",
        "flutter-build-release",
        "flutter-ci-cd",
        "flutter-code-review",
        "flutter-dependency-upgrades",
        "flutter-device-testing",
        "flutter-figma-workflow",
        "flutter-in-app-purchases",
        "flutter-localization",
        "flutter-navigation",
        "flutter-networking",
        "flutter-openapi-client",
        "flutter-notifications",
        "flutter-observability",
        "flutter-package-development",
        "flutter-performance",
        "flutter-persistence",
        "flutter-platform-integration",
        "flutter-product-analytics",
        "flutter-responsive-layout",
        "flutter-runtime-debugging",
        "flutter-security",
        "flutter-state-management",
        "flutter-testing",
        "flutter-text-rendering",
        "flutter-ui-design",
        "flutter-ui-patterns",
        "flutter-visual-effects",
        "flutter-webview",
    },
    "flutter-core-skills": {
        "dart-concurrency",
        "dart-language",
        "flutter-ai-integration",
        "flutter-architecture",
        "flutter-authentication",
        "flutter-dependency-upgrades",
        "flutter-networking",
        "flutter-openapi-client",
        "flutter-persistence",
        "flutter-state-management",
        "flutter-testing",
    },
    "flutter-ui-skills": {
        "flutter-accessibility",
        "flutter-animation",
        "flutter-figma-workflow",
        "flutter-localization",
        "flutter-navigation",
        "flutter-responsive-layout",
        "flutter-text-rendering",
        "flutter-ui-design",
        "flutter-ui-patterns",
        "flutter-visual-effects",
    },
    "flutter-engineering-skills": {
        "flutter-app-workflow",
        "flutter-authentication",
        "flutter-background-execution",
        "flutter-build-release",
        "flutter-ci-cd",
        "flutter-code-review",
        "flutter-dependency-upgrades",
        "flutter-device-testing",
        "flutter-in-app-purchases",
        "flutter-notifications",
        "flutter-observability",
        "flutter-package-development",
        "flutter-performance",
        "flutter-platform-integration",
        "flutter-product-analytics",
        "flutter-runtime-debugging",
        "flutter-security",
        "flutter-testing",
        "flutter-webview",
    },
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        frontmatter_text, body = text[4:].split("\n---\n", 1)
    except ValueError as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error

    metadata: dict[str, str] = {}
    for line in frontmatter_text.splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, body


def local_link_errors(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in LINK_PATTERN.findall(text):
        clean_target = target.split("#", 1)[0]
        if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
            continue
        if clean_target.startswith("/"):
            errors.append(f"{path.relative_to(ROOT)} uses absolute local link: {target}")
            continue
        resolved = (path.parent / clean_target).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)} has broken local link: {target}")
    return errors


def repository_markdown_paths() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*.md")
        if not IGNORED_LINK_DIRECTORIES.intersection(path.relative_to(ROOT).parts)
    ]


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"], warnings, 0, 0

    try:
        metadata, body = parse_frontmatter(skill_file)
    except ValueError as error:
        return [f"{skill_dir.name}: {error}"], warnings, 0, 0

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name is {name!r}")
    if not NAME_PATTERN.fullmatch(name):
        errors.append(f"{skill_dir.name}: invalid skill name")
    if not description:
        errors.append(f"{skill_dir.name}: missing description")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{skill_dir.name}: description exceeds {MAX_DESCRIPTION} characters")
    if not body.strip():
        errors.append(f"{skill_dir.name}: empty instructions")

    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > 300:
        warnings.append(f"{skill_dir.name}: SKILL.md is {line_count} lines")
    errors.extend(local_link_errors(skill_file))

    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        linked = {target.split("#", 1)[0] for target in LINK_PATTERN.findall(skill_file.read_text(encoding="utf-8"))}
        for reference in references_dir.rglob("*"):
            if reference.is_file():
                relative = reference.relative_to(skill_dir).as_posix()
                if relative not in linked:
                    errors.append(f"{skill_dir.name}: unlinked reference {relative}")
                errors.extend(local_link_errors(reference))

    for child in skill_dir.iterdir():
        if child.is_dir() and child.name not in {"evals", "references"} and not any(child.rglob("*")):
            warnings.append(f"{skill_dir.name}: empty subdirectory {child.name}/")

    eval_path = skill_dir / "evals" / "cases.json"
    if not eval_path.is_file():
        errors.append(f"{skill_dir.name}: missing evals/cases.json")
        return errors, warnings, len(description), 0

    try:
        cases = load_json(eval_path)
    except (json.JSONDecodeError, OSError) as error:
        errors.append(f"{skill_dir.name}: invalid eval JSON: {error}")
        return errors, warnings, len(description), 0
    if not isinstance(cases, list) or len(cases) < 2:
        errors.append(f"{skill_dir.name}: requires at least two eval cases")
        return errors, warnings, len(description), 0

    names: set[str] = set()
    for index, case in enumerate(cases):
        label = f"{skill_dir.name} eval {index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{label}: must be an object")
            continue
        case_name = case.get("name")
        if not isinstance(case_name, str) or not NAME_PATTERN.fullmatch(case_name):
            errors.append(f"{label}: invalid stable name")
        elif case_name in names:
            errors.append(f"{label}: duplicate name {case_name}")
        else:
            names.add(case_name)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label}: missing prompt")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or not expectations:
            errors.append(f"{label}: expectations must be a non-empty list")
        else:
            for exp_idx, item in enumerate(expectations):
                if isinstance(item, str):
                    if not item.strip():
                        errors.append(f"{label} expectation {exp_idx + 1}: must not be empty string")
                elif isinstance(item, dict):
                    text = item.get("text")
                    if not isinstance(text, str) or not text.strip():
                        errors.append(f"{label} expectation {exp_idx + 1}: must have non-empty 'text'")
                    if "mandatory" in item and not isinstance(item["mandatory"], bool):
                        errors.append(f"{label} expectation {exp_idx + 1}: 'mandatory' must be boolean")
                    if "id" in item and (not isinstance(item["id"], str) or not item["id"].strip()):
                        errors.append(f"{label} expectation {exp_idx + 1}: 'id' must be non-empty string")
                    unknown_keys = set(item) - {"text", "id", "mandatory"}
                    if unknown_keys:
                        errors.append(f"{label} expectation {exp_idx + 1}: unknown keys {sorted(unknown_keys)}")
                else:
                    errors.append(f"{label} expectation {exp_idx + 1}: must be a string or object")

    return errors, warnings, len(description), len(cases)


def normalized_skill_paths(values: list[str]) -> set[str]:
    return {value.removeprefix("./").removeprefix("skills/") for value in values}


def validate_packages(skill_names: set[str]) -> list[str]:
    errors: list[str] = []
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    codex = load_json(ROOT / ".codex-plugin" / "plugin.json")
    codex_marketplace = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    tessl = load_json(ROOT / ".tessl-plugin" / "plugin.json")
    tessl_root = load_json(ROOT / "tessl.json")
    npm_package = load_json(ROOT / "package.json")

    versions = {
        marketplace.get("metadata", {}).get("version"),
        codex.get("version"),
        tessl.get("version"),
        npm_package.get("version"),
    }
    versions.update(plugin.get("version") for plugin in marketplace.get("plugins", []))
    if versions != {EXPECTED_VERSION}:
        errors.append(f"package versions are not aligned at {EXPECTED_VERSION}: {sorted(str(value) for value in versions)}")

    plugins = {plugin.get("name"): plugin for plugin in marketplace.get("plugins", [])}
    if set(plugins) != set(EXPECTED_BUNDLES):
        errors.append(
            "Claude bundle names do not match expected bundles: "
            f"expected {sorted(EXPECTED_BUNDLES)}, found {sorted(plugins)}"
        )
    for plugin_name, expected_members in EXPECTED_BUNDLES.items():
        plugin = plugins.get(plugin_name)
        if plugin is None:
            continue
        actual_members = normalized_skill_paths(plugin.get("skills", []))
        if actual_members != expected_members:
            errors.append(
                f"{plugin_name}: membership mismatch; "
                f"missing {sorted(expected_members - actual_members)}, "
                f"unexpected {sorted(actual_members - expected_members)}"
            )
        unknown = actual_members - skill_names
        if unknown:
            errors.append(f"{plugin_name}: unknown skills {sorted(unknown)}")

    all_bundle = plugins.get("all-flutter-skills")
    if all_bundle and normalized_skill_paths(all_bundle.get("skills", [])) != skill_names:
        errors.append("all-flutter-skills membership does not match public skills")

    if normalized_skill_paths(tessl.get("skills", [])) != skill_names:
        errors.append("Tessl skill membership does not match public skills")
    if tessl.get("name") != tessl_root.get("name"):
        errors.append("Tessl package names are not aligned")

    if codex.get("name") != "flutter-skills":
        errors.append("Codex plugin name must be flutter-skills")
    if codex.get("skills") != "./skills/":
        errors.append("Codex plugin must expose ./skills/")
    if any(field in codex for field in ("apps", "mcpServers")):
        errors.append("Codex plugin must not declare apps or MCP servers without companion files")
    codex_interface = codex.get("interface", {})
    required_interface = {
        "displayName": "Flutter Skills",
        "developerName": "thienqo",
        "category": "Developer Tools",
    }
    for field, expected in required_interface.items():
        if codex_interface.get(field) != expected:
            errors.append(f"Codex plugin interface {field} must be {expected!r}")
    if codex_interface.get("capabilities") != ["Skills"]:
        errors.append("Codex plugin capabilities must describe its Skills surface")

    codex_entries = codex_marketplace.get("plugins", [])
    if codex_marketplace.get("name") != "flutter-skills" or len(codex_entries) != 1:
        errors.append("Codex marketplace must contain the flutter-skills plugin")
    else:
        codex_entry = codex_entries[0]
        if codex_entry.get("name") != codex.get("name"):
            errors.append("Codex marketplace and plugin names are not aligned")
        if codex_entry.get("source") != {"source": "local", "path": "./"}:
            errors.append("Codex marketplace must resolve the repository-root plugin")
        if codex_entry.get("policy") != {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        }:
            errors.append("Codex marketplace policy is incomplete")
        if codex_entry.get("category") != "Developer Tools":
            errors.append("Codex marketplace category must be Developer Tools")

    if npm_package.get("name") != "@thiennc/flutter-skills":
        errors.append("npm package name must be @thiennc/flutter-skills")
    if npm_package.get("private") is True:
        errors.append("npm package must be publishable")
    if npm_package.get("bin") != {"flutter-skills": "bin/flutter-skills.mjs"}:
        errors.append("npm package must expose the flutter-skills executable")
    if npm_package.get("dependencies", {}).get("skills") != "1.5.23":
        errors.append("npm package must pin skills@1.5.23")
    if npm_package.get("publishConfig", {}).get("access") != "public":
        errors.append("npm package must publish with public access")
    if npm_package.get("publishConfig", {}).get("provenance") is not True:
        errors.append("npm package must publish provenance")
    return errors


def validate_routing_cases(skill_names: set[str]) -> tuple[list[str], int]:
    errors: list[str] = []
    path = ROOT / ".github" / "evals" / "routing-cases.json"
    try:
        cases = load_json(path)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        return [f"invalid routing evaluations: {error}"], 0
    if not isinstance(cases, list):
        return ["routing evaluations must be a list"], 0

    names: set[str] = set()
    for index, case in enumerate(cases):
        label = f"routing eval {index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{label}: must be an object")
            continue
        name = case.get("name")
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            errors.append(f"{label}: invalid stable name")
        elif name in names:
            errors.append(f"{label}: duplicate name {name}")
        else:
            names.add(name)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label}: missing prompt")

        groups: dict[str, set[str]] = {}
        for field in ("required", "optional", "forbidden"):
            values = case.get(field)
            if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
                errors.append(f"{label}: {field} must be a string list")
                groups[field] = set()
                continue
            groups[field] = set(values)
            unknown = groups[field] - skill_names
            if unknown:
                errors.append(f"{label}: {field} has unknown skills {sorted(unknown)}")
        if not groups.get("required"):
            errors.append(f"{label}: requires at least one skill")
        if groups.get("required", set()) & groups.get("optional", set()):
            errors.append(f"{label}: required and optional skills overlap")
        if (groups.get("required", set()) | groups.get("optional", set())) & groups.get("forbidden", set()):
            errors.append(f"{label}: allowed and forbidden skills overlap")
    return errors, len(cases)


def release_changelog_errors(changelog: str) -> list[str]:
    match = re.search(
        rf"^## {re.escape(EXPECTED_VERSION)} - (\d{{4}}-\d{{2}}-\d{{2}})\s*$",
        changelog,
        re.MULTILINE,
    )
    if match:
        try:
            dt.date.fromisoformat(match.group(1))
        except ValueError:
            pass
        else:
            return []
    return [
        f"release metadata requires '## {EXPECTED_VERSION} - YYYY-MM-DD'; "
        "the version must not remain Unreleased"
    ]


def validate_documentation(
    skill_names: set[str],
    eval_total: int,
    routing_eval_total: int,
    release: bool = False,
) -> list[str]:
    errors: list[str] = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    try:
        catalog_section = readme.split("## Catalog", 1)[1].split("## Quality", 1)[0]
    except IndexError:
        errors.append("README is missing Catalog or Quality section")
    else:
        catalog_names = set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", catalog_section))
        if catalog_names != skill_names:
            errors.append(
                "README catalog mismatch; "
                f"missing {sorted(skill_names - catalog_names)}, "
                f"unexpected {sorted(catalog_names - skill_names)}"
            )

    expected_snippets = [
        f"Agent%20Skills-{len(skill_names)}-",
        f"**{len(skill_names)} skills**",
        f"**{eval_total} behavior-focused evaluation cases**",
        f"**{routing_eval_total} cross-catalog routing cases**",
    ]
    for snippet in expected_snippets:
        if snippet not in readme:
            errors.append(f"README is not synchronized; missing {snippet!r}")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"^## {re.escape(EXPECTED_VERSION)}(?:\s|$)", changelog, re.MULTILINE):
        errors.append(f"CHANGELOG is missing version {EXPECTED_VERSION}")
    if release:
        errors.extend(release_changelog_errors(changelog))
    return errors


def validate_repository(
    release: bool = False,
) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    skill_names = {path.name for path in skill_dirs}
    if len(skill_names) != EXPECTED_SKILL_COUNT:
        errors.append(f"expected {EXPECTED_SKILL_COUNT} public skills, found {len(skill_names)}")

    description_total = 0
    eval_total = 0
    for skill_dir in skill_dirs:
        skill_errors, skill_warnings, description_size, eval_count = validate_skill(skill_dir)
        errors.extend(skill_errors)
        warnings.extend(skill_warnings)
        description_total += description_size
        eval_total += eval_count

    if description_total > MAX_COMBINED_DESCRIPTION:
        errors.append(f"combined discovery descriptions exceed {MAX_COMBINED_DESCRIPTION} characters")

    try:
        errors.extend(validate_packages(skill_names))
    except (FileNotFoundError, json.JSONDecodeError) as error:
        errors.append(f"invalid package metadata: {error}")

    routing_errors, routing_eval_total = validate_routing_cases(skill_names)
    errors.extend(routing_errors)
    if eval_total != EXPECTED_EVAL_COUNT:
        errors.append(f"expected {EXPECTED_EVAL_COUNT} behavior evals, found {eval_total}")
    if routing_eval_total != EXPECTED_ROUTING_EVAL_COUNT:
        errors.append(
            f"expected {EXPECTED_ROUTING_EVAL_COUNT} routing evals, found {routing_eval_total}"
        )
    errors.extend(
        validate_documentation(
            skill_names, eval_total, routing_eval_total, release=release
        )
    )

    for markdown in repository_markdown_paths():
        errors.extend(local_link_errors(markdown))

    return errors, warnings, {
        "skills": len(skill_names),
        "evals": eval_total,
        "routing_evals": routing_eval_total,
        "description_characters": description_total,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release",
        action="store_true",
        help="require finalized release metadata such as a dated changelog entry",
    )
    args = parser.parse_args()
    errors, warnings, counts = validate_repository(release=args.release)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Validated {counts['skills']} skills, {counts['evals']} behavior eval cases, "
        f"{counts['routing_evals']} routing eval cases, "
        f"and {counts['description_characters']} discovery-description characters."
    )
    if warnings:
        print(f"Validation passed with {len(warnings)} advisory warning(s).")
    else:
        print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
