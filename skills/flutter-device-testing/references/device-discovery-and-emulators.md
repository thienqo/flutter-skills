# Device Discovery and Emulators

Use this reference for decisions shared by Android, Apple, browser, desktop, and physical targets. Load the platform-specific reference before issuing native commands.

## Discover and resolve one target

Inspect `pubspec.yaml`, Flutter and Dart constraints, enabled platform folders, flavors, entrypoints, and the repository's existing test harness. Treat supplied target facts as constraints and confirm them rather than silently selecting a more convenient device.

```sh
flutter devices
flutter emulators
```

Use `flutter doctor -v` when a required target or toolchain is unavailable, not as a substitute for reading the actual failure. Select by stable runtime identifier when multiple targets exist. Record a safe label, target kind, OS/runtime, and whether the target is:

- **reused**: user-owned or long-lived; preserve apps, data, snapshots, and unrelated overrides;
- **task-created disposable**: created for this task; retain its identifier internally and remove it only when cleanup was planned;
- **physical**: preserve user data and do not publish the raw serial or UDID by default.

Use the identifier for commands, but prefer the safe label in reports and shared artifacts.

## Establish readiness before the flow

Starting a virtual target and listing a connected device are different milestones. Before launching or asserting:

1. Wait until the selected runtime reports ready, with a bounded timeout.
2. Confirm the flavor-specific Android application ID or Apple bundle identifier.
3. Confirm the intended build is installed, or install it through the project's established Flutter/build workflow.
4. Confirm any required fixture, account, permission, locale, orientation, and network state.
5. For a warm scenario, explicitly prove the intended app process and foreground/background UI state before sending the trigger.

Do not infer readiness from a fixed sleep. If the target never becomes ready, retain the focused boot/tool error and stop rather than erasing it as a default recovery step.

## Preserve state and ownership

Never factory reset, wipe, erase, recreate, uninstall from, or clear application data on a reused or physical target merely to obtain a clean state. Those operations destroy local databases, caches, preferences, accounts, or snapshots. Prefer app-owned reset hooks, seeded disposable fixtures, or a task-created target. If destructive cleanup is genuinely required, resolve the exact target and application, explain the lost state, and obtain the necessary authorization.

For location, appearance, status bar, orientation, permissions, network shaping, accessibility settings, or other overrides:

- record the prior state when the platform exposes it, otherwise track exactly what the task changed;
- restore the prior state or clear only task-created overrides in failure-safe cleanup;
- do not claim that directly granting or revoking a permission proves the real prompt, rationale, or permanently-denied flow.

## Choose the interaction layer

- Use Dart and Flutter MCP inspection or `package:integration_test` for Flutter-owned widgets and semantic assertions.
- Use `adb` or `simctl` for bounded platform state and lifecycle control.
- Use the native-capable automation stack already present in the repository for permission dialogs, notification trays, external account pickers, or platform views. Do not add a framework without a project-specific need and compatibility review.
- Read [semantic UI inspection](semantic-ui-inspection.md) before driving a live app through the platform accessibility tree.
- Prefer stable keys, semantics/accessibility identifiers, or visible text contracts over coordinates. Bound waits on observable state rather than sleeping.

An OS command accepting a deep link or notification payload proves only trigger acceptance. Assert the destination, Back behavior, restored state, and allowed side effects inside the application.

## Retain proportionate evidence

Keep focused evidence that can be tied to the tested build:

- safe target label, target kind, OS/runtime, and physical-versus-virtual status;
- Flutter version, build mode, flavor, entrypoint, and non-secret define names when relevant;
- execution surface and data source as separate fields;
- named scenario, lifecycle state, permission/override state, assertions, and timestamps;
- filtered logs, test output, screenshots, video, or traces only when they prove the claim.

Do not retain secrets, URI queries, accounts, personal data, raw physical-device identifiers, or unrelated log history. A simulator or emulator can prove supported functional behavior, but not representative hardware performance, GPU behavior, camera/sensor fidelity, OEM differences, or production provider delivery.

## Platform routing

- Read [Android emulator operations](android-emulator-operations.md) for Android readiness, application state, logs, screenshots, permissions, and snapshots.
- Read [iOS Simulator operations](ios-simulator-operations.md) for Simulator boot, application state, logs, captures, privacy, location, and simulated push.

## Sources

- [Flutter CLI](https://docs.flutter.dev/reference/flutter-cli)
- [Flutter integration testing concepts](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Android Emulator command line](https://developer.android.com/studio/run/emulator-commandline)
- [Running apps on simulated or physical Apple devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices)
