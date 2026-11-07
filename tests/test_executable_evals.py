import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
SCRIPT = SCRIPTS_DIR / "run_executable_evals.py"
SPEC = importlib.util.spec_from_file_location("run_executable_evals", SCRIPT)
assert SPEC and SPEC.loader
EXECUTABLE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXECUTABLE)


class ExecutableEvalTests(unittest.TestCase):
    def test_specialist_discovery_is_selective_and_library_changes_are_forbidden(self):
        catalog = {
            "flutter-app-workflow": {"instructions": "Coordinate.", "resources": {}},
            "flutter-testing": {
                "description": "Test Flutter behavior.",
                "instructions": "Run focused tests.",
                "resources": {"references/checks.md": "Keep assertions strong."},
            },
        }
        case = {
            "skill": "flutter-app-workflow",
            "available_skills": ["flutter-testing"],
            "allowed_changes": ["lib"],
            "prompt": "Fix the feature.",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            EXECUTABLE.stage_skill_library(root, case, catalog)
            before = EXECUTABLE.snapshot(root)
            self.assertIn(".eval-skills/flutter-testing/references/checks.md", before)
            self.assertIn(
                "flutter-testing/SKILL.md", (root / ".eval-skills/catalog.md").read_text()
            )
            prompt = EXECUTABLE.build_prompt(case, catalog)
            self.assertIn(".eval-skills/catalog.md", prompt)
            self.assertNotIn("Run focused tests.", prompt)
            path = root / ".eval-skills/flutter-testing/SKILL.md"
            path.write_text("Weakened checks.")
            changes = EXECUTABLE.changed_paths(before, EXECUTABLE.snapshot(root))
            self.assertEqual(changes, [".eval-skills/flutter-testing/SKILL.md"])
            self.assertFalse(
                EXECUTABLE.path_is_allowed(changes[0], case["allowed_changes"])
            )

    def test_specialist_library_rejects_unknown_or_duplicate_skills(self):
        catalog = {"dart-concurrency": {"resources": {}}}
        case = {
            "name": "bad-library",
            "skill": "dart-concurrency",
            "prompt": "Fix it",
            "fixture": "dart-concurrency-latest-wins",
            "allowed_changes": ["lib"],
            "available_skills": ["missing", "missing", "dart-concurrency"],
            "checks": [{"command": ["dart", "analyze", "lib"]}],
        }
        errors = EXECUTABLE.validate_case(case, catalog)
        self.assertTrue(any("unknown available_skills" in error for error in errors))
        self.assertTrue(any("duplicate available_skills" in error for error in errors))
        self.assertTrue(any("already injected" in error for error in errors))

    def test_only_locked_offline_flutter_dependency_setup_is_allowlisted(self):
        case = {
            "name": "dependencies",
            "skill": "dart-concurrency",
            "prompt": "Fix it",
            "fixture": "dart-concurrency-latest-wins",
            "allowed_changes": ["lib"],
            "checks": [{"command": EXECUTABLE.OFFLINE_FLUTTER_PREPARE}],
        }
        catalog = {"dart-concurrency": {"resources": {}}}
        self.assertEqual(EXECUTABLE.validate_case(case, catalog), [])
        for command in [["flutter", "pub", "publish"], ["flutter", "pub", "get"]]:
            case["checks"] = [{"command": command}]
            self.assertTrue(
                any(
                    "subcommand is not allowed" in error
                    for error in EXECUTABLE.validate_case(case, catalog)
                )
            )

    def test_rejects_traversal_and_non_allowlisted_commands(self):
        catalog = {"dart-concurrency": {"resources": {}}}
        case = {
            "name": "unsafe",
            "skill": "dart-concurrency",
            "prompt": "Fix it",
            "fixture": "../outside",
            "allowed_changes": ["../tests"],
            "checks": [{"command": ["bash", "-c", "true"]}],
        }
        errors = EXECUTABLE.validate_case(case, catalog)
        self.assertTrue(any("safe relative path" in error for error in errors))
        self.assertTrue(any("executable is not allowed" in error for error in errors))

    def test_rejects_allowlisted_runtime_with_external_path(self):
        catalog = {"dart-concurrency": {"resources": {}}}
        case = {
            "name": "unsafe-path",
            "skill": "dart-concurrency",
            "prompt": "Fix it",
            "fixture": "missing",
            "allowed_changes": ["lib"],
            "checks": [{"command": ["dart", "run", "/tmp/untrusted.dart"]}],
        }
        errors = EXECUTABLE.validate_case(case, catalog)
        self.assertTrue(any("outside the fixture" in error for error in errors))

    def test_changed_paths_must_stay_within_declared_owners(self):
        self.assertTrue(EXECUTABLE.path_is_allowed("lib/latest.dart", ["lib"]))
        self.assertFalse(EXECUTABLE.path_is_allowed("bin/verify.dart", ["lib"]))
        self.assertFalse(EXECUTABLE.path_is_allowed("lib-other/file.dart", ["lib"]))

    def test_snapshot_ignores_generated_flutter_cache_but_tracks_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".dart_tool").mkdir()
            (root / ".dart_tool" / "package_config.json").write_text("generated")
            (root / "build").mkdir()
            (root / "build" / "output.bin").write_bytes(b"generated")
            (root / "lib" / "build").mkdir(parents=True)
            (root / "lib" / "build" / "source.dart").write_text("tracked")
            (root / "pubspec.yaml").write_text("name: fixture\n")
            (root / "pubspec.lock").write_text("pinned\n")
            self.assertEqual(
                sorted(EXECUTABLE.snapshot(root)),
                ["lib/build/source.dart", "pubspec.lock", "pubspec.yaml"],
            )

    def test_execute_case_rejects_agent_changes_to_verifier(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixtures = root / "fixtures"
            fixture = fixtures / "case"
            (fixture / "lib").mkdir(parents=True)
            (fixture / "bin").mkdir()
            (fixture / "lib" / "code.dart").write_text("broken\n", encoding="utf-8")
            (fixture / "bin" / "verify.dart").write_text("verify\n", encoding="utf-8")
            case = {
                "name": "case",
                "skill": "dart-concurrency",
                "prompt": "Fix it",
                "resources": [],
                "fixture": "case",
                "allowed_changes": ["lib"],
                "checks": [{"command": ["dart", "analyze", "lib"]}],
            }
            catalog = {
                "dart-concurrency": {
                    "instructions": "Keep latest results.",
                    "resources": {},
                }
            }

            class Agent:
                def run_in_workspace(self, prompt, workspace):
                    (workspace / "lib" / "code.dart").write_text("fixed\n", encoding="utf-8")
                    (workspace / "bin" / "verify.dart").write_text("weakened\n", encoding="utf-8")
                    return "done"

            baseline = [
                {
                    "name": "analyze",
                    "command": ["dart", "analyze", "lib"],
                    "exit_code": 1,
                    "stdout": "",
                    "stderr": "expected failure",
                    "passed": False,
                }
            ]
            with (
                patch.object(EXECUTABLE, "FIXTURES_DIR", fixtures),
                patch.object(EXECUTABLE, "run_checks", return_value=baseline),
            ):
                result = EXECUTABLE.execute_case(case, catalog, Agent())
            self.assertFalse(result["passed"])
            self.assertEqual(result["forbidden_changes"], ["bin/verify.dart"])
            self.assertEqual(result["checks"], [])


if __name__ == "__main__":
    unittest.main()
