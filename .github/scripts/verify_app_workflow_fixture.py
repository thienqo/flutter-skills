#!/usr/bin/env python3
"""Prove feature acceptance checks reject defects at each collaborating boundary."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from verify_responsive_fixture import check


ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE = ROOT / ".github" / "evals" / "executable"
FIXTURE = EXECUTABLE / "fixtures" / "app-workflow-task-completion"
ORACLE = EXECUTABLE / "oracles" / "app-workflow-task-completion"
SOURCES = {
    "task_repository.dart": "data",
    "task_controller.dart": "state",
    "task_screen.dart": "ui",
}


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="app-workflow-fixture-proof-") as directory:
        workspace = Path(directory) / "feature"
        shutil.copytree(FIXTURE, workspace, ignore=shutil.ignore_patterns(".dart_tool", "build"))
        check(workspace, ["flutter", "pub", "get", "--offline", "--enforce-lockfile"])
        check(workspace, ["flutter", "analyze", "--no-pub"])
        check(
            workspace,
            ["flutter", "test", "--no-pub", "--reporter=expanded", "--plain-name", "repository preserves"],
            fails_with="Invoice reviewed by server",
        )
        print("Seeded repository contract failure: caught")

        for name, owner in SOURCES.items():
            shutil.copy2(ORACLE / name, workspace / "lib" / owner / name)
        check(workspace, ["dart", "format", "--output=none", "--set-exit-if-changed", "lib", "test"])
        check(workspace, ["flutter", "analyze", "--no-pub"])
        check(workspace, ["flutter", "test", "--no-pub", "--reporter=expanded"])
        print("Corrected data/state/UI feature: 7 acceptance scenarios passed")

        controller_path = workspace / "lib" / "state" / "task_controller.dart"
        controller = controller_path.read_text(encoding="utf-8")
        mutations = [
            (
                "duplicate submit",
                "_disposed || saving || task.completed",
                "_disposed || task.completed",
                "controller announces pending",
                "Expected: ['task-7']",
            ),
            (
                "late result after disposal",
                "if (_disposed) return;\n      task = confirmed;",
                "task = confirmed;",
                "disposed controller ignores late success",
                "Expected: same instance",
            ),
        ]
        for label, old, new, test_name, marker in mutations:
            if controller.count(old) != 1:
                raise AssertionError(f"{label} mutation no longer matches the oracle")
            controller_path.write_text(controller.replace(old, new), encoding="utf-8")
            check(
                workspace,
                ["flutter", "test", "--no-pub", "--reporter=expanded", "--plain-name", test_name],
                fails_with=marker,
            )
            print(f"Seeded {label}: caught")
        controller_path.write_text(controller, encoding="utf-8")

        screen = workspace / "lib" / "ui" / "task_screen.dart"
        text = screen.read_text(encoding="utf-8")
        old = "if (controller.error != null) Text(controller.error!),"
        if text.count(old) != 1:
            raise AssertionError("Missing-error mutation no longer matches the oracle")
        screen.write_text(text.replace(old, ""), encoding="utf-8")
        check(
            workspace,
            ["flutter", "test", "--no-pub", "--reporter=expanded", "--plain-name", "UI shows a recoverable error"],
            fails_with="Unable to complete task. Please retry.",
        )
        print("Seeded hidden recovery error: caught")


if __name__ == "__main__":
    main()
