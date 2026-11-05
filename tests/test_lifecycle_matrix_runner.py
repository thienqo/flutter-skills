import importlib.util
import json
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    ROOT
    / "skills"
    / "flutter-device-testing"
    / "scripts"
    / "run_lifecycle_matrix.py"
)
SPEC = importlib.util.spec_from_file_location("run_lifecycle_matrix", RUNNER_PATH)
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class LifecycleMatrixRunnerTests(unittest.TestCase):
    def test_cli_defaults_to_a_redacted_dry_run(self):
        with tempfile.TemporaryDirectory() as directory:
            matrix_path = Path(directory) / "matrix.json"
            matrix_path.write_text(
                json.dumps(
                    {
                        "platform": "android",
                        "device_id": "emulator-5554",
                        "app_id": "com.example.app",
                        "scenarios": [
                            {
                                "name": "warm-link",
                                "lifecycle": "warm",
                                "uri": "myapp://orders/42?token=secret",
                                "assert": [
                                    {
                                        "name": "order destination",
                                        "argv": [sys.executable, "-c", "pass"],
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(RUNNER_PATH), str(matrix_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            report = json.loads(completed.stdout)
            self.assertEqual(report["status"], "planned")
            self.assertEqual(report["schema_version"], 2)
            self.assertNotIn("device_id", report["target"])
            trigger = report["scenarios"][0]["steps"][0]
            self.assertNotIn("token=secret", json.dumps(trigger))

    def test_builds_platform_commands_without_a_shell(self):
        self.assertEqual(
            RUNNER.deep_link_command(
                "android", "emulator-5554", "com.example.app", "myapp://orders/42"
            ),
            [
                "adb",
                "-s",
                "emulator-5554",
                "shell",
                "am",
                "start",
                "-W",
                "-a",
                "android.intent.action.VIEW",
                "-d",
                "myapp://orders/42",
                "com.example.app",
            ],
        )
        self.assertEqual(
            RUNNER.deep_link_command(
                "ios", "A-SIMULATOR-ID", "com.example.app", "myapp://orders/42"
            ),
            ["xcrun", "simctl", "openurl", "A-SIMULATOR-ID", "myapp://orders/42"],
        )

    def test_android_device_shell_receives_one_literal_uri(self):
        uri = "myapp://orders/42?a=1&b=2;printf BAD"
        args = RUNNER.deep_link_command(
            "android", "emulator-5554", "com.example.app", uri
        )
        # Model adb's join and the Android shell with a local, inert am stub.
        shell_program = 'am() { printf "%s\\n" "$@"; }; ' + " ".join(args[4:])
        completed = subprocess.run(
            ["/bin/sh", "-c", shell_program], capture_output=True, text=True, check=True
        )
        self.assertEqual(completed.stdout.splitlines()[-2:], [uri, "com.example.app"])
        unusual_id = "com.example.app;printf BAD"
        commands = RUNNER.preflight_commands("android", "emulator-5554", unusual_id)
        self.assertEqual(shlex.split(" ".join(commands[1][1][4:])), ["pm", "path", unusual_id])
        stop = RUNNER.lifecycle_command("android", "emulator-5554", unusual_id)
        self.assertEqual(shlex.split(" ".join(stop[4:])), ["am", "force-stop", unusual_id])

    def test_report_redacts_entire_cookie_and_urls_in_hook_output(self):
        log = (
            "Cookie: session=FAKE_SESSION; refresh=FAKE_REFRESH\n"
            "callback https://user:FAKE_PASSWORD@example.invalid/path"
            "?code=FAKE_CODE#FAKE_FRAGMENT"
        )
        report = RUNNER.run_step(
            "hook", [sys.executable, "-c", "import sys; print(sys.argv[1])", log], 5, True
        )
        self.assertEqual(
            report["output_tail"].strip(),
            "Cookie: [REDACTED]\ncallback https://example.invalid/path",
        )
        self.assertEqual(
            RUNNER.safe_command(["https://user:FAKE_PASSWORD@example.invalid/?token=FAKE_TOKEN"]),
            ["https://example.invalid/"],
        )

    def test_cleanup_runs_after_a_failed_assertion(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "cleaned"
            matrix = RUNNER.validate_matrix(
                {
                    "platform": "android",
                    "device_id": "test-device",
                    "app_id": "com.example.app",
                    "scenarios": [
                        {
                            "name": "warm-notification",
                            "lifecycle": "warm",
                            "trigger": {
                                "name": "no-op provider fixture",
                                "argv": [sys.executable, "-c", "pass"],
                            },
                            "assert": [
                                {
                                    "name": "destination",
                                    "argv": [sys.executable, "-c", "raise SystemExit(7)"],
                                }
                            ],
                            "after": [
                                {
                                    "name": "remove fixture",
                                    "argv": [
                                        sys.executable,
                                        "-c",
                                        f"from pathlib import Path; Path({str(marker)!r}).touch()",
                                    ],
                                }
                            ],
                        }
                    ],
                }
            )
            report = RUNNER.run_matrix(matrix, execute=True)
            self.assertEqual(report["status"], "failed")
            self.assertTrue(marker.exists())
            self.assertEqual(
                report["scenarios"][0]["steps"][-1]["status"], "passed"
            )

    def test_ios_cold_prepare_accepts_an_already_stopped_app(self):
        result = RUNNER.normalize_lifecycle_result(
            "ios",
            {
                "name": "prepare: terminate app",
                "status": "failed",
                "exit_code": 3,
                "output_tail": "The application is not running",
            },
        )
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["note"], "app was already stopped")

    def test_rejects_a_scenario_without_semantic_assertions(self):
        with self.assertRaisesRegex(
            RUNNER.MatrixError, "assert must contain at least one verification step"
        ):
            RUNNER.validate_matrix(
                {
                    "platform": "android",
                    "device_id": "emulator-5554",
                    "app_id": "com.example.app",
                    "scenarios": [
                        {
                            "name": "launch-only",
                            "lifecycle": "warm",
                            "uri": "myapp://orders/42",
                        }
                    ],
                }
            )

    def test_report_redacts_tokens_and_uri_queries(self):
        self.assertNotIn(
            "secret-value",
            RUNNER.redact("Authorization: Bearer secret-value"),
        )
        self.assertEqual(
            RUNNER.safe_uri("myapp://orders/42?token=secret-value"),
            "myapp://orders/42",
        )
        self.assertEqual(
            RUNNER.safe_command(
                [
                    "tool",
                    "Authorization: Bearer secret-value",
                    "myapp://orders/42?token=x",
                ]
            ),
            ["tool", "Authorization: Bearer [REDACTED]", "myapp://orders/42"],
        )

    def test_report_redacts_before_truncating_output(self):
        secret = "synthetic-secret-value"
        for prefix in ("Authorization: Bearer ", "access_token=", "refresh_token: "):
            with self.subTest(prefix=prefix):
                output = prefix + secret + "\n" + "x" * (4000 - len(secret) - 1)
                with mock.patch.object(
                    RUNNER.subprocess,
                    "run",
                    return_value=subprocess.CompletedProcess(
                        ["fixture"], 0, stdout=output, stderr=""
                    ),
                ):
                    result = RUNNER.run_step("fixture", ["fixture"], 1, True)
                self.assertEqual(result["status"], "passed")
                self.assertNotIn(secret, result["output_tail"])
                self.assertLessEqual(len(result["output_tail"]), 4000)

    def test_redacts_device_id_when_truncation_splits_it(self):
        device_id = "synthetic-device-id"
        output = device_id + "\n" + "x" * 3990
        redacted = RUNNER.redact(output, sensitive_values=(device_id,))
        self.assertNotIn("device-id", redacted)
        self.assertLessEqual(len(redacted), 4000)

    def test_timeout_output_is_redacted_before_truncation(self):
        secret = "synthetic-secret-value"
        output = ("Authorization: Bearer " + secret + "\n" + "x" * 3970).encode()
        with mock.patch.object(
            RUNNER.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(["fixture"], 1, output=output),
        ):
            result = RUNNER.run_step("fixture", ["fixture"], 1, True)
        self.assertEqual(result["status"], "timeout")
        self.assertNotIn(secret, result["output_tail"])
        self.assertLessEqual(len(result["output_tail"]), 4000)

    def test_version_two_requires_explicit_warm_precondition(self):
        with self.assertRaisesRegex(
            RUNNER.MatrixError, "precondition must verify the warm app and UI state"
        ):
            RUNNER.validate_matrix(
                {
                    "matrix_version": 2,
                    "platform": "android",
                    "device_id": "emulator-5554",
                    "target_kind": "android-emulator",
                    "target_label": "pixel-api-staging",
                    "app_id": "com.example.app",
                    "scenarios": [
                        {
                            "name": "warm-link",
                            "lifecycle": "warm",
                            "uri": "myapp://orders/42",
                            "assert": [
                                {
                                    "name": "destination",
                                    "argv": [sys.executable, "-c", "pass"],
                                }
                            ],
                        }
                    ],
                }
            )

    def test_safe_target_label_cannot_repeat_hidden_device_id(self):
        with self.assertRaisesRegex(
            RUNNER.MatrixError, "target_label must not repeat device_id"
        ):
            RUNNER.validate_matrix(
                {
                    "matrix_version": 2,
                    "platform": "ios",
                    "device_id": "SIMULATOR-UDID",
                    "target_kind": "ios-simulator",
                    "target_label": "SIMULATOR-UDID",
                    "app_id": "com.example.app",
                    "scenarios": [
                        {
                            "name": "cold-link",
                            "lifecycle": "cold",
                            "uri": "myapp://orders/42",
                            "assert": [
                                {
                                    "name": "destination",
                                    "argv": [sys.executable, "-c", "pass"],
                                }
                            ],
                        }
                    ],
                }
            )

    def test_version_two_dry_run_adds_preflight_and_hides_device_id(self):
        matrix = RUNNER.validate_matrix(
            {
                "matrix_version": 2,
                "platform": "android",
                "device_id": "physical-serial-123",
                "target_kind": "android-physical",
                "target_label": "checkout-test-phone",
                "app_id": "com.example.app.staging",
                "context": {
                    "flavor": "staging",
                    "build_mode": "debug",
                    "data_source": "local mock API",
                },
                "scenarios": [
                    {
                        "name": "cold-link",
                        "lifecycle": "cold",
                        "uri": "myapp://orders/42?token=secret",
                        "assert": [
                            {
                                "name": "destination",
                                "argv": [sys.executable, "-c", "pass"],
                            }
                        ],
                    }
                ],
            }
        )
        report = RUNNER.run_matrix(matrix, execute=False)
        rendered = json.dumps(report)
        self.assertEqual(report["status"], "planned")
        self.assertEqual(len(report["preflight"]), 2)
        self.assertEqual(
            report["target"],
            {"label": "checkout-test-phone", "kind": "android-physical"},
        )
        self.assertNotIn("physical-serial-123", rendered)
        self.assertIn("[DEVICE_ID]", rendered)
        self.assertNotIn("token=secret", rendered)

    def test_version_two_preflight_failure_skips_scenarios(self):
        matrix = RUNNER.validate_matrix(
            {
                "matrix_version": 2,
                "platform": "android",
                "device_id": "emulator-5554",
                "target_kind": "android-emulator",
                "target_label": "pixel-api-staging",
                "app_id": "com.example.app",
                "scenarios": [
                    {
                        "name": "cold-link",
                        "lifecycle": "cold",
                        "uri": "myapp://orders/42",
                        "assert": [
                            {
                                "name": "destination",
                                "argv": [sys.executable, "-c", "pass"],
                            }
                        ],
                    }
                ],
            }
        )

        def fake_run_step(name, argv, timeout, execute, sensitive_values=()):
            if name == "preflight: target online":
                return {"name": name, "status": "passed", "output_tail": "device"}
            if name == "preflight: app installed":
                return {"name": name, "status": "passed"}
            self.fail(f"unexpected step after failed preflight: {name}")

        with mock.patch.object(RUNNER, "run_step", side_effect=fake_run_step):
            report = RUNNER.run_matrix(matrix, execute=True)

        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["preflight"][-1]["status"], "failed")
        self.assertEqual(report["scenarios"][0]["status"], "skipped")

    def test_device_id_can_be_retained_only_by_explicit_opt_in(self):
        matrix = RUNNER.validate_matrix(
            {
                "platform": "ios",
                "device_id": "SIMULATOR-UDID",
                "include_device_id": True,
                "app_id": "com.example.app",
                "scenarios": [
                    {
                        "name": "cold-link",
                        "lifecycle": "cold",
                        "uri": "myapp://orders/42",
                        "assert": [
                            {
                                "name": "destination",
                                "argv": [sys.executable, "-c", "pass"],
                            }
                        ],
                    }
                ],
            }
        )
        report = RUNNER.run_matrix(matrix, execute=False)
        self.assertEqual(report["target"]["device_id"], "SIMULATOR-UDID")


if __name__ == "__main__":
    unittest.main()
