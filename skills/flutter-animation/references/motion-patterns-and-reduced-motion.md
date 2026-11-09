# Motion Patterns and Reduced Motion

When implementing complex motion or addressing accessibility in Flutter, apply these practices:

## Staggered Animations
- Use a **single `AnimationController`** for sequential or overlapping animations.
- Define staggered timings by passing an `Interval` to a `CurvedAnimation`.
- Do not create multiple controllers unless the animations can independently change state.

## Physics-Based Animation
- Use `SpringSimulation` or `FrictionSimulation` for natural, interruptible gestures.
- Drive the animation using `AnimationController.animateWith(Simulation)`.
- Avoid hardcoded durations when physics simulations dictate the timing.

## Hero Transitions
- Keep each tag unique within a participating route subtree. The corresponding source and destination Heroes must share the same tag; making tags unique across the whole navigation stack prevents the intended flight.
- When a product appears more than once in one participating subtree, scope its tag to that visual context (e.g., `'$tabName-$productId'`) and pass the selected tag to the destination.
- **Tab shells and nested navigators**: Inspect which route subtrees participate in the owning Hero controller. Mounted tabs alone do not prove a collision. Scope duplicate tags within that collection or disable nonparticipating Heroes with `HeroMode`; verify forward and reverse flights as well as the absence of duplicate-tag assertions.

See the [Hero contract](https://api.flutter.dev/flutter/widgets/Hero-class.html) for matching tags and nested-navigator participation.

## Reduced Motion
- On Android, read Remove animations through `MediaQuery.disableAnimationsOf(context)`. On iOS, read Reduce Motion separately through `PlatformDispatcher.accessibilityFeatures.reduceMotion` when the resolved Flutter SDK exposes it. If the SDK does not expose the signal, use a compatible existing platform adapter or bridge the native `UIAccessibility.isReduceMotionEnabled` setting. Observe changes if the affected UI stays mounted. Keep `accessibleNavigation` for assistive interaction such as a running screen reader.
- Replace nonessential motion with immediate state changes or minimal fade transitions.
- Verify reduced motion with screen-reader mode off, and screen-reader mode with reduced motion off. Cover the iOS case where Reduce Motion is on and `disableAnimations` is false. Assert the same essential actions remain reachable and work after the decorative animation is suppressed.

## AnimatedSwitcher Identity
- `AnimatedSwitcher` treats the new child as the same child — and skips the transition — when `Widget.canUpdate` holds: same `runtimeType` and same `key`. Swapping between two widgets of the same type with no explicit key (two `Text` widgets, two instances of one custom widget) updates in place and no transition plays. Children of different types already animate without keys.
- When the widget type does not change, give each distinct state a stable distinguishing `Key` (such as `ValueKey(data.id)` or `ValueKey(stateName)`).

## Reusing Designed Animation Packages
- When a designer-produced animation asset exists (or the design team will deliver one) for a complex sequence — an illustrated loading state, an onboarding sequence, a mascot — check whether the project already depends on `rive` or `lottie` (or an equivalent asset-driven animation package) before hand-rolling the same result with `CustomPainter` or a long `AnimationController` sequence. Reusing the existing package keeps the asset editable by design tooling and avoids re-deriving timing curves by hand. If no asset exists and the motion is simple enough to express in code, hand-rolling with `AnimationController` is reasonable.
- A Rive or Lottie animation still needs the same lifecycle discipline as any other controller-driven motion: dispose any controller the package API has you create in the owning `State`'s `dispose()` — for `lottie`, the `AnimationController` passed as `controller:` (a loaded `LottieComposition` is plain data with no `dispose()`); for `rive`, the controller or file objects its current API documents as disposable — and respect reduced-motion preferences by showing a static frame or skipping playback.

## Ticker Leak Prevention
- Always call `dispose()` on `AnimationController` instances within the owning `State`'s `dispose()` method.
- Use `SingleTickerProviderStateMixin` for one controller, or `TickerProviderStateMixin` for multiple. Never leak tickers across route changes.

## Sources

- [Flutter reduced-motion signal](https://api.flutter.dev/flutter/dart-ui/AccessibilityFeatures/disableAnimations.html)
- [Flutter iOS Reduce Motion signal](https://api.flutter.dev/flutter/dart-ui/AccessibilityFeatures/reduceMotion.html)
- [Apple UIAccessibility Reduce Motion](https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled)
- [Flutter accessible navigation signal](https://api.flutter.dev/flutter/dart-ui/AccessibilityFeatures/accessibleNavigation.html)
