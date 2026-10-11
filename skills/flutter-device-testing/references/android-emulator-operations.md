# Android Emulator Operations

Use Flutter tooling for project-aware build and launch behavior, then use `adb` only for Android state that Flutter tooling does not own. Check the installed Flutter and Android command help before relying on fast-moving native syntax.

## Resolve, start, and wait

```sh
flutter emulators
flutter emulators --launch <emulator-id>
flutter devices
adb -s <serial> wait-for-device
adb -s <serial> shell getprop sys.boot_completed
```

Select the emulator by its Flutter emulator ID, then resolve the runtime serial reported by `flutter devices` or `adb devices -l`. Do not assume an AVD name is the runtime serial. Treat `wait-for-device` as transport readiness; also require `sys.boot_completed` to become `1` within a bounded loop before installing, launching, or asserting.

Prefer an existing suitable AVD. Before creating or updating one, inspect the project's minimum/target SDK, required ABI, Google APIs or Play Services needs, and available system images. Do not wipe an AVD or load a snapshot that overwrites newer user state unless the target is disposable or the data loss was explicitly approved.

## Confirm the application and launch contract

Resolve the application ID for the requested flavor from the Gradle configuration or generated build output. Do not infer it from the Dart package name.

```sh
adb -s <serial> get-state
adb -s <serial> shell pm path <application-id>
flutter run -d <serial> --flavor <flavor> -t <entrypoint>
```

Pass only defines already required by the project, and keep secrets out of command arguments and reports. If the test uses a prebuilt APK, verify that it was built for the requested flavor and mode before installing it through the repository's established command.

## Lifecycle and state

Use the narrowest operation that represents the scenario:

- Home/background and resume are different from killing the process.
- `am kill` represents eligible background-process death; it is not equivalent to user force-stop.
- `am force-stop` changes later intent, alarm, and background-delivery semantics. Use it only when the scenario is explicitly a force-stop or cold-entry case.
- Clearing package data or uninstalling destroys app-owned state and requires an explicit clean-state decision.

For deep links, target the selected serial and verify application behavior after Android accepts the intent:

```sh
adb -s <serial> shell am start -W \
  -a android.intent.action.VIEW \
  -d <uri> <application-id>
```

For Android App Links, separately verify domain association and resolver state when that is part of the claim. A successful `am start` does not prove navigation, authentication continuation, Back behavior, or exactly-once side effects.

## Permissions, configuration, and native UI

`pm grant` and `pm revoke` can prepare supported permission states, but they bypass the real request dialog. Test the actual dialog with the project's existing native-capable harness when prompt copy, choice handling, denial, limited access, or permanently-denied behavior matters.

Orientation, locale, font scale, accessibility, network shaping, battery, and other device-wide settings can affect unrelated applications and later tests. Read the current value first when possible and restore it in failure-safe cleanup. Prefer project/test APIs when they can isolate the state to the application.

Flutter `ValueKey`s work for Flutter test finders. Native black-box tools generally require stable semantics or accessibility identifiers exposed to the platform tree; do not fall back to screen coordinates without an explicit, unavoidable reason.

## Appearance, font scale, and demo mode

```sh
adb -s <serial> shell cmd uimode night            # read current value first
adb -s <serial> shell cmd uimode night yes
adb -s <serial> shell settings get system font_scale
adb -s <serial> shell settings put system font_scale 2.0
adb -s <serial> shell settings put global sysui_demo_allowed 1
adb -s <serial> shell am broadcast -a com.android.systemui.demo -e command enter
adb -s <serial> shell am broadcast -a com.android.systemui.demo -e command exit
```

Use dark mode, font scale, and System UI demo mode for theme, large-text, and consistent screenshot passes. These are device-wide: record the prior values, restore them in failure-safe cleanup, and exit demo mode even after failures. `settings get` may print `null` for an unset value; restore that by deleting the key the task added (`settings delete system font_scale`) rather than writing a guessed default.

## Inspect persisted app data

```sh
adb -s <serial> shell run-as <application-id> ls shared_prefs
adb -s <serial> shell run-as <application-id> cat shared_prefs/<file>.xml
```

`run-as` works only for debuggable builds. It confirms what the app persisted without root or backups. Check the plugin version and API before assuming file names, since newer plugin APIs may use a different store. Treat the contents as user data and keep secrets out of reports.

## Focused diagnostics and artifacts

Start with Flutter output, then narrow Android logs to the application process or relevant tags:

```sh
flutter logs -d <serial>
adb -s <serial> shell pidof <application-id>
adb -s <serial> logcat --pid=<pid>
flutter screenshot -d <serial>
adb -s <serial> exec-out screencap -p
```

Start log capture before reproducing a launch crash. Bound log and video capture, stop it after the scenario, and retain only the relevant interval. Record whether the screenshot came from Flutter tooling or the full Android display when system UI is material.

## Evidence boundary

Android Emulator is useful for repeatable functional, API-level, lifecycle, permission-state, and integration checks. Verify performance, thermal behavior, camera and sensor fidelity, OEM-specific behavior, hardware-backed security, background restrictions that depend on a vendor build, and release readiness on representative physical hardware. Use profile mode and route performance attribution to `flutter-performance`.

## Sources

- [Flutter CLI](https://docs.flutter.dev/reference/flutter-cli)
- [Run apps on Android Emulator](https://developer.android.com/studio/run/emulator)
- [Android Emulator command line](https://developer.android.com/studio/run/emulator-commandline)
- [Android Emulator snapshots](https://developer.android.com/studio/run/emulator-snapshots)
- [Android Debug Bridge](https://developer.android.com/tools/adb)
- [Create deep links](https://developer.android.com/training/app-links/create-deeplinks)
