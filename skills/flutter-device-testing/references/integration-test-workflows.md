# Integration Test Workflows

Integration tests verify complete user journeys and native plugin interactions on a live target device using `package:integration_test`.

## Project Setup

Inspect `pubspec.yaml`, the Flutter SDK constraint, existing integration tests, flavors, entrypoints, and any native-capable harness before changing setup. Preserve an adequate existing test stack. When the task requires a durable Flutter integration test and the SDK package is absent, add `integration_test` under `dev_dependencies`:
```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
```

Create test entrypoints inside the `integration_test/` directory at the project root (e.g., `integration_test/app_test.dart`):

Inspect the imported entrypoint before choosing the startup call. The example below assumes the app exposes `Future<void> main()`. Await asynchronous initialization before the first pump. For a synchronous `void main()`, call it without `await`. If the app declares `void main() async`, prefer extracting initialization into an awaitable `Future<void>` bootstrap shared by production and tests so the test can observe completion.

<!-- checked-snippet: integration-test-checkout -->
```dart
import 'package:flutter/foundation.dart' show Key;
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Complete checkout flow on target device', (tester) async {
    await app.main(); // This example assumes Future<void> main().
    await tester.pumpAndSettle();

    // Interact with UI using standard finder and tap APIs
    final startButton = find.byKey(const Key('start_checkout'));
    expect(startButton, findsOneWidget);
    await tester.tap(startButton);
    await tester.pumpAndSettle();

    // Verify destination behavior
    expect(find.text('Order Summary'), findsOneWidget);
  });
}
```

## Running Integration Tests

Execute integration tests against a resolved target and pass the project's exact flavor, entrypoint, and non-secret defines. Inspect `flutter test --help` for the pinned SDK when syntax is uncertain:
```sh
flutter test integration_test/app_test.dart -d <device-id> --flavor staging
```

Some projects use a host driver for screenshots, response data, performance traces, web execution, or device-lab packaging. Preserve the established `flutter test` or `flutter drive` workflow instead of mechanically converting it. Record which command and build mode actually ran.

## Flutter UI versus native system UI

`package:integration_test` uses Flutter test APIs and cannot operate arbitrary native permission dialogs, notification trays, account pickers, or platform views as Flutter widgets.

- Keep Flutter-owned interactions and assertions in `integration_test` with stable keys, text contracts, and semantic state.
- Use `adb` or `simctl` to prepare supported OS state only when the prompt itself is not under test.
- When the native UI must be exercised, use the repository's already adopted native-capable automation layer, such as Patrol, Maestro, Appium, XCUITest, or UIAutomator. Add or migrate a framework only after checking project compatibility and maintenance cost; none is a universal default.
- Native black-box tools generally need identifiers exposed through the platform accessibility tree. A Flutter `ValueKey` is not automatically a native accessibility identifier. Check the pinned Flutter SDK before using version-specific semantics APIs.

Directly granting a permission can prove Flutter behavior under that state, but it does not prove the system prompt, rationale, limited access, permanently-denied behavior, usage-description metadata, or user interaction with the dialog. Cover those boundaries separately when required.

## Best Practices and Determinism

- **Semantic Finders**: Prefer finding widgets by `ValueKey` or explicit text rather than fragile relative coordinates or deep widget-tree paths.
- **Startup Boundary**: Match the call to the actual entrypoint signature. Do not leave a returned startup `Future` unawaited, and do not mechanically add `await` to a synchronous entrypoint.
- **Startup Regression Coverage**: When extracting or changing bootstrap behavior, test that dependencies finish before the app is mounted and that an initialization failure remains observable without mounting a partially initialized app. Keep one integration smoke assertion proving the awaited startup reaches the expected first screen; inject or fake the initialization boundary for deterministic failure coverage instead of contacting live services.
- **Wait Boundaries**: Use `pumpAndSettle()` only when the screen can actually settle. Prefer an explicit observable condition with a bounded timeout for periodic animations, asynchronous native transitions, or continuously updating screens. Do not use arbitrary sleeps as readiness checks.
- **Deep Link Verification**: Test deep link invocation on target devices using platform commands:
  - Android: `adb -s <device-id> shell am start -W -a android.intent.action.VIEW -d "'myapp://product/123?source=test&mode=preview'" <application-id>`. The inner quotes are for the device shell. Use the lifecycle runner for dynamic URI values.
  - iOS Simulator: `xcrun simctl openurl <device-id> "myapp://product/123"`
- **Cleanup**: Ensure integration tests tear down only accounts, fixtures, overrides, or temporary files created by the test, including after failures.
- **Evidence**: A passing test proves the named assertions on the reported execution surface and data source. It does not upgrade a simulator to hardware, a mock to staging, or a launch command to destination correctness.

For a repeated cold/warm deep-link or notification-entry matrix, use [lifecycle entry matrix](lifecycle-entry-matrix.md) and keep project-specific setup and assertions in test-owned hooks.

For performance measurements, run the appropriate established driver in profile mode on representative physical hardware and route attribution to `flutter-performance`; simulator or emulator timing is not release-performance evidence.

## Sources

- [Flutter integration testing concepts](https://docs.flutter.dev/cookbook/testing/integration/introduction)
- [Check app functionality with an integration test](https://docs.flutter.dev/testing/integration-tests)
- [Flutter testing overview](https://docs.flutter.dev/testing/overview)
- [Flutter Key API](https://api.flutter.dev/flutter/foundation/Key-class.html)
