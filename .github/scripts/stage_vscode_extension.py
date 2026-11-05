#!/usr/bin/env python3
"""Stage the Flutter Skills VS Code extension from a Git revision."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--publisher", default="thienqo")
    args = parser.parse_args()

    version = json.loads(subprocess.check_output(
        ["git", "show", f"{args.ref}:package.json"], cwd=ROOT
    ))["version"]
    payload = subprocess.check_output(
        ["git", "archive", args.ref, "skills", "LICENSE", "assets/antigravity-icon.png"],
        cwd=ROOT,
    )
    args.destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(payload)) as bundle:
        skill_payload = (
            member for member in bundle
            if Path(member.name).parts[2:3] != ("evals",)
        )
        bundle.extractall(args.destination, members=skill_payload, filter="data")

    skill_files = sorted(args.destination.glob("skills/*/SKILL.md"))
    if not skill_files:
        parser.error("the selected revision contains no skills")

    manifest = {
        "name": "flutter-skills",
        "displayName": "Flutter Skills",
        "publisher": args.publisher,
        "version": version,
        "description": "Agent skills for building, reviewing, testing, and releasing Flutter and Dart apps.",
        "engines": {"vscode": "^1.109.0"},
        "categories": ["AI", "Chat"],
        "keywords": ["flutter", "dart", "copilot", "agent-skills"],
        "icon": "assets/antigravity-icon.png",
        "license": "BSD-3-Clause",
        "files": ["skills", "assets", "README.md", "LICENSE"],
        "repository": {"type": "git", "url": "https://github.com/thienqo/flutter-skills.git"},
        "contributes": {
            "chatSkills": [
                {"path": "./" + path.relative_to(args.destination).as_posix()}
                for path in skill_files
            ]
        },
    }
    (args.destination / "package.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.destination / "README.md").write_text(
        "# Flutter Skills\n\n"
        f"{len(skill_files)} agent skills for building, reviewing, testing, and releasing Flutter and Dart apps.\n\n"
        "Install this extension, open Copilot Chat, and ask for a workflow or invoke a skill by name, "
        "such as `/flutter-app-workflow`. The skills follow your project's architecture and packages.\n\n"
        "See the [full catalog and source](https://github.com/thienqo/flutter-skills).\n"
    )


if __name__ == "__main__":
    main()
