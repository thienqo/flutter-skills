#!/usr/bin/env python3
"""Analyze the marked integration-test snippet in its pinned Flutter fixture."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from verify_responsive_fixture import check


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = Path("skills/flutter-device-testing/references/integration-test-workflows.md")
FIXTURE = ROOT / ".github/maintainer/verification/integration-test-snippet"
SNIPPET = re.compile(
    r"^<!-- checked-snippet: integration-test-checkout -->\n"
    r"```dart\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def main() -> int:
    markdown = (ROOT / REFERENCE).read_text(encoding="utf-8")
    matches = list(SNIPPET.finditer(markdown))
    if len(matches) != 1 or not matches[0][1].strip():
        raise SystemExit(f"{REFERENCE}: expected exactly one nonempty marked Dart snippet")
    match = matches[0]
    line_offset = markdown.count("\n", 0, match.start(1))

    with tempfile.TemporaryDirectory(prefix="flutter-skill-snippet-") as directory:
        workspace = Path(directory) / "example"
        shutil.copytree(FIXTURE, workspace, ignore=shutil.ignore_patterns(".dart_tool", "build"))
        example = workspace / "integration_test" / "checkout_test.dart"
        example.parent.mkdir()
        example.write_text(match[1], encoding="utf-8")
        check(workspace, ["flutter", "pub", "get", "--enforce-lockfile"])
        result = subprocess.run(
            ["dart", "analyze", "--format=machine", str(example)],
            cwd=workspace,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
        for diagnostic in (result.stdout + result.stderr).splitlines():
            parts = diagnostic.split("|", 7)
            if len(parts) == 8 and Path(parts[3]).resolve() == example.resolve():
                severity, _, _, _, line, column, _, message = parts
                print(f"{REFERENCE}:{line_offset + int(line)}:{column}: {severity.lower()}: {message}")
            else:
                print(diagnostic)
    if result.returncode == 0:
        print(f"{REFERENCE}: integration-test snippet passed analysis")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
