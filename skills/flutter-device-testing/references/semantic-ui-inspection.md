# Semantic UI Inspection on a Live Target

Use this reference when an agent must read or drive a running Flutter app from outside the Dart process: exploratory checks, smoke flows without an integration harness, or confirming what assistive technology and black-box tools actually see. Prefer `package:integration_test` or Dart and Flutter MCP inspection when the project already supports them; this layer is for observing the platform accessibility tree.

## Read structure before pixels

Flutter paints into one platform view. Native tools see Flutter widgets only through the semantics tree that the engine bridges to the platform accessibility API. Reading that tree is cheaper and more reliable than reading screenshots:

- A filtered accessibility dump lists element roles, labels, identifiers, values, and frames in a few hundred tokens; a full-resolution screenshot costs thousands and still needs interpretation.
- Use screenshots for visual evidence, layout or theme review, and bug reports. Downscale or crop them to the region that matters.

```sh
# iOS Simulator (idb, only if already installed or approved for the task)
idb ui describe-all --udid <UDID> --json

# Android emulator or device
adb -s <serial> shell uiautomator dump /sdcard/<task-dump>.xml
adb -s <serial> exec-out cat /sdcard/<task-dump>.xml
adb -s <serial> shell rm /sdcard/<task-dump>.xml
```

Reduce the dump to interactive or labeled nodes (role, label, identifier, enabled, bounds) before reasoning over it. Do not paste raw dumps into reports.

## Act, then re-read

1. Locate the target node by identifier first, then by exact label, then by role and index. Use raw coordinates only when no semantic target exists, and state that in the report.
2. Act at the center of the node's frame or bounds (`idb ui tap`, `adb shell input tap`), or type into a focused field (`idb ui text`, `adb shell input text`).
3. Re-read the tree and confirm the expected node, value, or screen appeared within a bounded retry. A zero exit code from a tap or text command proves only that the event was sent.

Keep credentials out of `input text` arguments where shell history or retained logs could expose them; use project test accounts.

## Stable identifiers

`Semantics(identifier: ...)` is exposed as `accessibilityIdentifier` on iOS and as the view resource ID on Android, so the same identifier works in idb, UiAutomator, and other native black-box tools without changing what screen readers announce. `ValueKey` and `Key` are visible only to Flutter finders. Check the project's minimum Flutter SDK and existing naming convention before adding identifiers, and do not rewrite user-facing labels just to ease automation.

## When the tree is empty or opaque

If the dump shows a single full-screen Flutter view or no actionable nodes while the screen visibly has controls, lead with the diagnosis below, even when the user asks for a pixel tap. Offer a coordinate tap only after naming the likely cause and the durable fix, label it as a temporary fallback in the response and the report, and verify its outcome without the tree. Before a blind tap on a payment, deletion, or other irreversible control, confirm the build uses a test backend and account.

1. Confirm the app is foregrounded and past launch; re-read after a bounded wait.
2. Suspect that the semantics tree is not enabled. Platform embeddings historically build the bridge only when the OS reports an assistive technology or automation client, and behavior varies by Flutter version and platform. Test the installed SDK instead of assuming.
3. Enable semantics only from a debug or automation entrypoint the project owns or the user approves, for example by holding the handle returned by `SemanticsBinding.instance.ensureSemantics()` for the app lifetime. Never add this to the production entry path, and report the entrypoint used.
4. If the tree exists but nodes lack labels or roles, the widgets are missing semantics. Route that fix, and any new `Semantics(identifier: ...)` on the control, to `flutter-accessibility` instead of permanently automating by coordinates.

Merged semantics (`MergeSemantics`, `ListTile`, labeled buttons) collapse children into one node with a joined label. Lazy lists expose only built children, so scroll and re-read rather than searching for off-screen items. Platform views expose their own native tree.

## Sources

- [SemanticsProperties.identifier](https://api.flutter.dev/flutter/semantics/SemanticsProperties/identifier.html)
- [Flutter accessibility testing](https://docs.flutter.dev/ui/accessibility/accessibility-testing)
- [Add set semantics enabled API and wire iOS a11y bridge (flutter#161265)](https://flutter.googlesource.com/mirrors/flutter/+/26037dff87ade9d9dee04cc2ef90b3fe5cf0faf3)
- [idb commands](https://fbidb.io/docs/commands)
- [Android Debug Bridge](https://developer.android.com/tools/adb)
- Approach adapted from [conorluddy/ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill) (MIT)
