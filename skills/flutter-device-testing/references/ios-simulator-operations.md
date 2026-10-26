# iOS Simulator Operations

Use Flutter tooling for project-aware build and launch behavior, then use `xcrun simctl` for Simulator-specific lifecycle and state. Run `xcrun simctl help <subcommand>` before using version-sensitive flags.

## Resolve, boot, and wait

```sh
flutter emulators
xcrun simctl list -j devices available
xcrun simctl bootstatus <UDID> -b
flutter devices
```

Resolve one available device and runtime by UDID. Prefer an already booted suitable Simulator. `bootstatus -b` boots if necessary and waits for readiness; use a bounded outer timeout in automation. Do not hardcode a device name because the same name can exist under multiple runtimes.

Create or clone a Simulator only when the test needs isolation that an existing target cannot safely provide. Record ownership immediately so cleanup deletes only the task-created device. Never use `erase all`, delete broad CoreSimulator directories, or erase an unrelated Simulator as routine recovery.

## Confirm the application and launch contract

Resolve the bundle identifier for the requested flavor/scheme from the Xcode configuration or built application. Do not infer it from the Dart package name.

```sh
flutter run -d <UDID> --flavor <flavor> -t <entrypoint>
xcrun simctl get_app_container <UDID> <bundle-id> app
xcrun simctl launch <UDID> <bundle-id>
```

`get_app_container` is a non-destructive installed-app check. Install a simulator-built `.app`, not a device `.ipa`, when a prebuilt artifact is used. Reinstalling can preserve app data; uninstalling and erasing do not, so do not use them for routine cleanup.

## Lifecycle, links, and logs

```sh
xcrun simctl terminate <UDID> <bundle-id>
xcrun simctl openurl <UDID> <uri>
xcrun simctl spawn <UDID> log stream \
  --predicate 'process == "Runner"'
```

Match termination and relaunch to the requested cold or warm lifecycle. For a warm scenario, use a project-owned semantic precondition to prove the intended screen and foreground/background state before the trigger. A successful `openurl` proves only that Simulator accepted the URL; assert destination, authentication continuation, Back behavior, and side effects in the application.

Prefer subsystem/category or process predicates over an unfiltered log stream. Start capture before reproduction and stop it after a bounded interval.

## Privacy, location, appearance, and push

Use `simctl privacy`, `location`, `ui`, and `status_bar` only after checking the installed command help. Target one UDID and bundle identifier. Record the prior state when available; otherwise track the task-created override and clear it after pass or failure.

Direct permission grant or revocation prepares state but does not prove the real prompt, usage-description configuration, rationale, limited-access UI, or denial path. Use the repository's existing native-capable test harness when the native dialog itself matters.

`simctl push` tests local payload parsing, presentation, tap handling, and navigation in Simulator. It does not prove APNs registration, credentials, entitlement configuration, provider acceptance, network delivery, background policy on hardware, or every push type. Keep those claims for the appropriate provider and physical-device verification.

## Appearance, text size, and status bar

```sh
xcrun simctl ui <UDID> appearance            # read current value first
xcrun simctl ui <UDID> appearance dark
xcrun simctl ui <UDID> content_size           # read current value first
xcrun simctl ui <UDID> content_size accessibility-extra-extra-extra-large
xcrun simctl status_bar <UDID> override --time 9:41 --batteryState charged --batteryLevel 100
xcrun simctl status_bar <UDID> clear
```

Use these to run a theme, Dynamic Type, or screenshot-consistency pass without editing app code. Record each value before changing it and restore it afterward; `status_bar clear` removes every override, so use it only when the task applied the override. Pair large text sizes with `flutter-responsive-layout` or `flutter-accessibility` when overflow is the subject.

## Inspect persisted app data

```sh
xcrun simctl get_app_container <UDID> <bundle-id> data
plutil -p "<data-container>/Library/Preferences/<bundle-id>.plist"
```

Read-only inspection of the data container confirms what the app persisted, for example values written through `NSUserDefaults`-backed plugins. Check the plugin version and API before assuming key names or storage location. Treat container contents as user data: do not copy tokens or personal data into reports, and do not edit files in place to fake a state the app should produce.

## Screenshots and video

```sh
flutter screenshot -d <UDID>
xcrun simctl io <UDID> screenshot <path.png>
xcrun simctl io <UDID> recordVideo <path.mov>
```

`flutter screenshot` defaults to the target's native full-screen capture; use its SDK-supported Skia mode with a VM service URL only when Flutter-rendered output specifically is required. Simulator IO also captures the device display and is useful when system chrome or native UI is part of the evidence. Bound video recording, stop it reliably, and use task-specific artifact paths. Clear only task-created status-bar, location, appearance, permission, or media state.

## Evidence boundary

Simulator is useful for repeatable functional, lifecycle, layout, permission-state, local push-payload, and integration checks. It does not reproduce physical-device performance or every hardware feature. Verify release performance, Metal/GPU behavior, camera capture, Bluetooth, NFC, sensors, hardware-backed security, real APNs delivery, and device-only background behavior on representative physical hardware. Use profile or release-like mode and route benchmark attribution to `flutter-performance`.

## Sources

- [Flutter CLI](https://docs.flutter.dev/reference/flutter-cli)
- [Running apps on simulated or physical Apple devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices)
- [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build)
- Local `xcrun simctl help` for the installed Xcode command contract
