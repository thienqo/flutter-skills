# Lifecycle entry matrix

Use a replayable matrix when a deep link or notification tap crosses application lifecycle, authentication, navigation, or remote-data boundaries. Select only rows that can expose failures in the changed behavior.

## Scenario design

Give every row a stable name and state its entry kind, cold or warm lifecycle, account/auth fixture, current UI state, trigger identity, data behavior, expected destination, Back outcome, and allowed side effects. Include duplicate delivery when multiple listeners or initial-message handoff can receive the same intent.

Useful rows include cold signed-in entry, cold signed-out continuation after login, warm entry over a dialog or sheet, duplicate link or notification, slow/error destination API, and account switch between receipt and interaction. A launch command only proves that the OS accepted the trigger; use semantic integration assertions, running-app inspection, or focused screenshots/logs to prove the destination and side effects.

## Runner

`scripts/run_lifecycle_matrix.py` orchestrates one Android emulator/device or iOS Simulator. For iOS, `app_id` is the bundle identifier. It defaults to a dry run, invokes commands as argv without a host shell and quotes arguments passed through the Android device shell, bounds each step, runs target and installed-app preflight for version 2 matrices, redacts common token and cookie output and strips URL credentials, queries, and fragments from report text, hides the target identifier by default, and writes machine-readable evidence.

Every scenario hook, including `precondition`, inherits the top-level `timeout_seconds` bound. Every `after` hook is failure-safe cleanup: the runner invokes it from a `finally` path after a pass, failed `before`, failed `precondition`, failed trigger or assertion, timeout, or command error. State both guarantees when reviewing a plan. Keep restoration and fixture cleanup in `after` rather than at the end of an assertion hook, and make the cleanup itself idempotent because its failure marks the scenario failed.

Use `matrix_version: 2` for new matrices. Version 2 requires an explicit `precondition` command for every warm scenario so a fixture-only setup cannot be mislabeled as a warm app state. Version 1 remains accepted for existing callers but does not gain the stronger warm-state guarantee.

Each project supplies shell-free `before`, `trigger`, `assert`, and `after` commands for its own auth fixture, provider send, API delay, semantic assertion, and cleanup. Put credentials in the command's existing environment or secret store; never place them in the matrix or command arguments.

The `tool/...` commands below illustrate project-owned hooks; replace them with commands already provided by the target repository.

The report can retain a bounded output tail from each hook. Make hooks emit already sanitized evidence and avoid full payloads, personal data, device identifiers, or secrets; automatic token redaction is only a fallback for common patterns. Give the target a safe `target_label`. Set `include_device_id` only for a private artifact whose reproducibility requirement outweighs identifier exposure; it remains false by default.

```json
{
  "matrix_version": 2,
  "platform": "android",
  "device_id": "emulator-5554",
  "target_kind": "android-emulator",
  "target_label": "pixel-api-staging",
  "include_device_id": false,
  "app_id": "com.example.app",
  "timeout_seconds": 60,
  "context": {
    "flavor": "staging",
    "build_mode": "debug",
    "entrypoint": "lib/main_staging.dart",
    "data_source": "local mock API",
    "provider": "local notification fixture"
  },
  "scenarios": [
    {
      "name": "cold-signed-out-order-link",
      "lifecycle": "cold",
      "before": [
        {"name": "seed signed-out fixture", "argv": ["tool/test-state", "signed-out"]},
        {"name": "delay order API", "argv": ["tool/test-server", "delay", "orders", "1500"]}
      ],
      "uri": "myapp://orders/42",
      "assert": [
        {"name": "login then order and Back", "argv": ["tool/assert-flow", "login-order-back", "42"]}
      ],
      "after": [
        {"name": "failure-safe clear test state", "argv": ["tool/test-state", "clear"]}
      ]
    },
    {
      "name": "warm-duplicate-notification-over-dialog",
      "lifecycle": "warm",
      "before": [
        {"name": "show dialog fixture", "argv": ["tool/test-state", "dialog-open"]}
      ],
      "precondition": [
        {"name": "app is warm with dialog visible", "argv": ["tool/assert-runtime-state", "foreground", "dialog-open"]}
      ],
      "trigger": {
        "name": "send notification fixture",
        "argv": ["tool/send-test-notification", "order-42"]
      },
      "trigger_count": 2,
      "assert": [
        {"name": "one navigation effect", "argv": ["tool/assert-effect-count", "order-42", "1"]}
      ],
      "after": [
        {"name": "failure-safe clear test state", "argv": ["tool/test-state", "clear"]}
      ]
    }
  ]
}
```

The optional `context` object accepts only `flavor`, `build_mode`, `entrypoint`, `data_source`, `provider`, and `os_runtime`, with non-empty string values. Do not invent adjacent names such as `provider_layer`; the runner rejects unknown fields during the dry run.

The built-in version 2 preflight checks that the selected Android target is online and that `pm path` resolves `app_id`, or that the selected iOS Simulator is booted and `get_app_container` resolves the bundle. Custom hooks remain responsible for account, fixture, provider, and semantic UI readiness.

Review the plan, confirm the target label, target kind, application identity, allowed context fields, warm preconditions, per-step timeout, failure-safe cleanup, and every hook stay within the task's existing authorization, then execute it:

```sh
python3 path/to/run_lifecycle_matrix.py matrix.json
python3 path/to/run_lifecycle_matrix.py matrix.json --execute --report artifacts/lifecycle-report.json
```

Do not proceed merely because the dry-run JSON was printed. After replacing every placeholder, require the dry run to exit with status 0, confirm its report status is `planned`, and inspect the redacted preflight and scenario commands. Only then add `--execute`. If schema validation or plan generation fails, correct the matrix rather than bypassing the gate.

Keep reports only when they contain redacted, useful evidence and the repository's artifact policy permits them. State the safe target label and kind, OS/runtime when supplied by the hook, flavor/build, lifecycle rows, data source, provider layer, and failed or skipped assertions in the final report. Do not publish the raw target identifier by default.

## Sources

- [Flutter deep linking](https://docs.flutter.dev/ui/navigation/deep-linking)
- [Flutter: set up universal links for iOS](https://docs.flutter.dev/cookbook/navigation/set-up-universal-links)
- [Android: create deep links](https://developer.android.com/training/app-links/create-deeplinks)
