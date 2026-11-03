# Semantics and Screen Readers

Screen readers (TalkBack on Android, VoiceOver on iOS/macOS) translate Flutter's semantics tree into spoken feedback and braille output. Proper semantics configuration ensures all users can navigate and operate the app.

## The Semantics Tree

Flutter automatically builds a semantics tree from built-in widgets (e.g., `Text`, `ElevatedButton`, `Checkbox`). Only add manual `Semantics` widgets when custom interactive or composite components are used.

### 1. `Semantics`
Use to annotate custom interactive elements with label, hint, value, button flag, or custom actions:
```dart
Semantics(
  button: true,
  enabled: isActionable,
  label: 'Add item to shopping cart',
  hint: 'Double tap to activate',
  onTap: onAddToCart,
  child: CustomCartButton(),
)
```

### 2. `MergeSemantics`
Merge a subtree of related nodes into a single semantic focus node. Essential for list tiles or cards containing an icon, title, and subtitle so the screen reader speaks the entire group together instead of forcing three separate swipes:
```dart
MergeSemantics(
  child: Row(
    children: [
      Icon(Icons.check_circle),
      SizedBox(width: 8),
      Text('Order Placed'),
    ],
  ),
)
```

### 3. `ExcludeSemantics` / `BlockSemantics`
- **`ExcludeSemantics`**: Hide purely decorative elements (icons with adjacent text, background illustrations, spacer art) from the screen reader to reduce audio clutter.
- **`BlockSemantics`**: Drop semantics behind a modal surface (dialog, bottom sheet, drawer) to prevent screen readers from focusing on backdrop widgets.

## Dynamic Announcements

Prefer semantic state changes, including a suitable live region, for ordinary asynchronous feedback. Use an explicit announcement only when the system does not already announce the change.

A save confirmation, form result, or loading-finished message is ordinary feedback. Show it as visible status text inside `Semantics(liveRegion: true)`. On Android and iOS a live region produces a polite announcement without moving focus, though the OS may skip it while already speaking. Verify web behavior on the pinned SDK with a screen reader. Do not pick an explicit announcement for it per platform. Keep `sendAnnouncement` for changes that have no visible semantic node. A request to fix a failing `announce` call does not mean an announcement is the right mechanism: fix the call, then say whether the feedback should move to a semantic update. On SDKs supporting the current view-aware API:
```dart
if (MediaQuery.supportsAnnounceOf(context)) {
  SemanticsService.sendAnnouncement(
    View.of(context),
    'Changes saved successfully', // Use the project's localized message.
    Directionality.of(context),
    assertiveness: Assertiveness.polite,
  );
}
```
- Obtain text direction from `Directionality.of(context)` instead of hardcoding LTR to preserve RTL locale support.
- Resolve the message through the originating window's localization context as well as its direction and view; windows can have different locale overrides. Do not use a global locale or context for window-owned feedback.
- Check the pinned SDK before using `sendAnnouncement` or `supportsAnnounceOf`. The deprecated `announce` API relies on an implicit view and is incompatible with multiple windows; retain a legacy path only when the supported SDK requires it and its single-view contract is satisfied.
- `assertiveness` currently affects web only. On Android, prefer semantic updates because explicit announcement events can disrupt TalkBack's speech queue. Avoid duplicate or repetitive announcements.

See [SemanticsService.sendAnnouncement](https://api.flutter.dev/flutter/semantics/SemanticsService/sendAnnouncement.html) and the [legacy API limitations](https://api.flutter.dev/flutter/semantics/SemanticsService/announce.html).

## Automated Verification

- `testWidgets` enables semantics by default and disposes its framework-owned handle after the callback. Prefer that default instead of opening a second handle:
  ```dart
  testWidgets('favorite toggle exposes its state', (tester) async {
    await tester.pumpWidget(const TestApp());
    expect(
      tester.getSemantics(find.byType(CustomCartButton)),
      matchesSemantics(...),
    );
  });
  ```
- If a test deliberately manages an additional semantics handle, register cleanup immediately so assertion or pump failures cannot leak it into later tests:
  ```dart
  final handle = tester.ensureSemantics();
  addTearDown(handle.dispose);
  ```
- Use `meetsGuideline(androidTapTargetGuideline)` and `meetsGuideline(iOSTapTargetGuideline)` in widget tests.
