# Lifecycle and Disposal

Proper disposal of state resources prevents memory leaks and unintended behavior across screens or sessions. Follow these rules for common patterns.

## Disposal Patterns

- **ChangeNotifier**: Implement `dispose()` and have the actual owner dispose it. A provider that creates the notifier may already do this. Remove a listener explicitly if the notifier outlives it.
- **Bloc/Cubit**: Clean up resources in `close()`. If the Bloc creates standard Dart Streams, ensure they are canceled here.
- **Riverpod**: For `autoDispose` providers, rely on Riverpod's internal cleanup, but explicitly register disposal callbacks via `ref.onDispose` for native resources or non-Riverpod listeners.

## Stream and Controller Cleanup

- Close any `StreamController` created locally. Do this in `dispose()` or the equivalent lifecycle teardown method.
- Cancel all active `StreamSubscription` instances when the class that created them is disposed. Do not rely on garbage collection for active subscriptions.

## Testing Lifecycle

- Remove the actual owner in a widget test when the resource is screen-scoped. Assert that removal triggers disposal, cancels owned subscriptions, and blocks late updates. A unit test that calls `dispose()` directly covers cleanup logic separately.
- Test that calling `dispose()` twice (if allowed by the framework) is safe or throws appropriately, and verify no updates are emitted post-disposal.

## Leak Patterns

- **Global Singletons**: Do not use global singletons or static variables as a substitute for clear scope boundaries and proper disposal. Global lifespans bypass tree lifecycle hooks.
- **Undisposed Controllers**: Missing `close()` calls on controllers or missing `cancel()` calls on subscriptions are the primary sources of leaks in Flutter apps. Review these carefully.

## Riverpod and Bloc disposal pitfalls

- **Riverpod state after an `await`**: Check the resolved version in `pubspec.lock`. In Riverpod 2.x, register cancellation or invalidate a captured lifetime token with `ref.onDispose` before the async gap. Guard both success and error before updating the notifier's `state`. Riverpod 3.0 introduced `Ref.mounted`. On versions that support it, capture the request's `Ref` before awaiting and check that instance before publishing. Use an operation identity when requests can supersede one another. Retain a disposal or generation guard for rebuilds on versions older than 3.2.0, which fixed `Ref.mounted` on stale refs after rebuild.
- Keep automatic disposal when a provider should end with its last listener. If the product requires temporary retention, use the supported `ref.keepAlive()` contract and close its returned link when retention ends. Test normal completion, owner removal while pending, and late success or error. Include provider recomputation when it can replace the in-flight request.
- **Bloc event ordering**: Choose an explicit event transformer (sequential, `restartable`/switch-latest, or `droppable`) for any handler that performs async work. Default concurrent event handling lets rapid repeated events run their async bodies out of order and call `emit` after the Bloc has moved on to a different state. Treat an `emit.isDone` guard as a secondary safeguard once the transformer is correct, not a substitute for choosing the right one.

## Sources

- [Flutter State disposal and listener cleanup](https://api.flutter.dev/flutter/widgets/State/dispose.html)
- [Riverpod 3.0 and Ref.mounted](https://riverpod.dev/docs/whats_new#refmounted)
- [Riverpod cancellation with ref.onDispose](https://riverpod.dev/docs/how_to/cancel)
- [Riverpod automatic disposal and retention](https://riverpod.dev/docs/concepts2/auto_dispose)
- [Riverpod 3.2.0 stale-ref fix](https://pub.dev/packages/riverpod/changelog#320---2026-01-17)
