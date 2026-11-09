# Geometry, Viewport, and Fixture Testing

Use this reference when components overlap, clip, leave the visible region, or become unreachable only at particular sizes, text scales, locales, keyboard states, or content states.

## Classify the failure

Separate three kinds of evidence:

1. A framework layout exception such as `RenderFlex` overflow identifies an incompatible constraint path.
2. Paint geometry can be wrong without an exception, such as a sticky action covering the final field or two independently positioned controls intersecting.
3. A component may look visible but be unreachable because another layer wins hit testing.

Preserve the first exception and inspect the constraint-owning ancestor before changing sizes. For silent visual overlap, identify the exact components and the product relationship they must satisfy.

## Define spatial contracts

Do not scan every render object and fail on any intersection. Parent and child boxes overlap by design, as do intentional `Stack`, badge, scrim, tooltip, floating-action, and decorative layers. Instead, assign stable keys or semantic finders to important components and define only relationships required by the screen:

- **Disjoint:** independent actions or content regions must not intersect.
- **Contained:** a child, focus indicator, or error message must remain inside its allowed viewport or surface.
- **Gap:** components must retain a product-defined minimum separation.
- **Intentional overlay:** name the allowed overlay and verify that underlying content has the required inset, scrolling, or alternate access path.
- **Reachable:** each required action must remain hit-testable and must produce its observable result.

After layout, `WidgetTester.getRect` is useful for disjoint, containment, and gap assertions when the relevant boxes are untransformed. For example:

```dart
final fieldRect = tester.getRect(find.byKey(const ValueKey('last-field')));
final actionRect = tester.getRect(find.byKey(const ValueKey('checkout-action')));

expect(
  fieldRect.overlaps(actionRect),
  isFalse,
  reason: 'The sticky action must not cover the final field',
);
expect(
  find.byKey(const ValueKey('checkout-action')).hitTestable(),
  findsOneWidget,
);
```

`getRect` constructs a rectangle from the transformed top-left and bottom-right corners. With rotation or skew, those two points can understate the extent. For an axis-aligned bound of a rotated or skewed box, take min and max coordinates across all four transformed corners in the same coordinate space. For actual overlap of rotated shapes, a bound is only a broad check. Pair geometry with hit testing or rendered evidence as appropriate, especially with clipping, opacity, and platform views. A center-point `hitTestable` check does not prove that the entire target is unobscured.

## Exercise a bounded viewport matrix

Build the matrix from product constraints rather than device model names. Include:

- the smallest supported logical viewport;
- one case immediately below and above each content breakpoint;
- a representative compact and wide size;
- portrait or landscape only where composition changes;
- normal and required enlarged text scales;
- keyboard or other `viewInsets` states when they affect the failure;
- safe-area or display-feature cases relevant to supported targets.

Before emitting or applying a runnable harness, inspect the project's pinned Flutter version, Dart constraint, and existing test helpers. Confirm that its SDK exposes the selected `TestFlutterView`, text-scaling, view-inset, and teardown APIs. When compatible APIs are supplied or confirmed, use them concretely in the harness. If the repository or SDK version is not supplied, label current-API snippets as conditional, name the compatibility inspection still required, and do not claim that they compile for the target project. Preserve an established compatible helper instead of introducing a second viewport harness. Run the focused test with the project's own Flutter SDK after implementation.

Set the test view explicitly and restore it after the test. Apply text scaling inside `MaterialApp.builder` so the fixture receives the same application shell while the scale varies:

```dart
final view = tester.view;
view.devicePixelRatio = 1;
view.physicalSize = const Size(320, 640);
addTearDown(view.reset);

await tester.pumpWidget(
  MaterialApp(
    builder: (context, child) => MediaQuery(
      data: MediaQuery.of(context).copyWith(
        textScaler: TextScaler.linear(2),
      ),
      child: child!,
    ),
    home: const CheckoutFixture.longContent(),
  ),
);
await tester.pump();
expect(tester.takeException(), isNull);
```

Keep the logical size consistent with `physicalSize / devicePixelRatio`. Use APIs compatible with the project's Flutter SDK; older projects may expose test-window configuration differently.

## Generate deterministic fixtures

Give the screen a fixture builder or existing dependency seams that can render relevant product states without network, wall-clock, random, or mutable global input. Prefer named fixtures such as typical, long localized content, loading, empty, validation error, and offline over one production-shaped mock graph.

Automate the high-risk combinations, not the full Cartesian product. For example, run typical content at every breakpoint, then pair the smallest viewport with long content, enlarged text, RTL, validation errors, and an open keyboard. Give each case a descriptive test name so a failure identifies its viewport and fixture.

For every case, assert the relevant contract:

- no layout exception;
- required components are present and within the allowed region;
- explicitly disjoint components do not overlap;
- scrollable content can reveal the last field or action;
- primary actions remain hit-testable and complete the intended interaction;
- breakpoint selection and state survive resizing when required.

Add a focused golden only when pixel output is a stable contract. Geometry tests prove selected spatial relationships; goldens or screenshots reveal unmodeled visual collisions; device tests prove system keyboard, platform view, safe-area, and OS chrome behavior. State which layer was actually exercised.

## Sources

- [WidgetController.getRect](https://api.flutter.dev/flutter/flutter_test/WidgetController/getRect.html)
- [Finder.hitTestable](https://api.flutter.dev/flutter/flutter_test/Finder/hitTestable.html)
- [TestFlutterView.physicalSize](https://api.flutter.dev/flutter/flutter_test/TestFlutterView/physicalSize.html)
- [TestFlutterView.devicePixelRatio](https://api.flutter.dev/flutter/flutter_test/TestFlutterView/devicePixelRatio.html)
- [Flutter adaptive and responsive best practices](https://docs.flutter.dev/ui/adaptive-responsive/best-practices)
