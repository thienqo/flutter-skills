# Stream Cancellation and Debouncing

Streams model sequences of asynchronous events over time. Failure to cancel subscriptions or handle race conditions between events is a major source of memory leaks and stale UI states.

## Subscription Lifecycle and Cancellation

- **Always Store and Cancel**: Never call `.listen()` without assigning the returned `StreamSubscription` to a variable that is explicitly cancelled in `dispose()`, `close()`, or during component unmount.
- **Cancel on Re-trigger**: When starting a new asynchronous operation from user input (e.g., search queries), define latest-wins behavior and prevent overlapping `cancel`/`listen` continuations. A generation token is one package-free option:
  ```dart
  int _searchGeneration = 0;
  Future<void>? _searchCancellation;

  Future<void> search(String query) async {
    final generation = ++_searchGeneration;
    final previous = _searchSubscription;
    _searchSubscription = null;
    if (previous != null) {
      _searchCancellation = Future<void>.microtask(previous.cancel);
    }
    final cancellation = _searchCancellation;
    try {
      await cancellation;
    } finally {
      if (identical(_searchCancellation, cancellation)) {
        _searchCancellation = null;
      }
    }

    if (generation != _searchGeneration) return;
    _searchSubscription = repository.search(query).listen((result) {
      if (generation == _searchGeneration) emit(result);
    });
  }
  ```
  All retriggers share pending cleanup even when the subscription field is empty. Schedule cancellation in a microtask so a synchronous cancellation callback can see the shared future if it retriggers search. Let cleanup errors reach the owner, which decides whether another search is safe. Clear only the future that finished so a later attempt can proceed without reusing a failed future or clearing a newer cleanup. Increment the generation before final teardown, cancel the stored subscription, and await any pending cleanup before releasing shared resources. Alternatively, serialize the whole cancel-and-listen transition or use switch-latest semantics already present in the project's stream stack. A busy flag can lose the newest query, and debounce alone reduces request frequency but does not guarantee ordering or ownership.
- **StreamController Ownership**: A controller must be closed by the class that instantiates it. Never leave a controller open after its consumers are unmounted. Check `isClosed` before adding events if emissions can race with disposal.

## Debouncing and Throttling

- **Debounce**: Delay event processing until a quiet period has elapsed. Essential for text input and auto-complete to avoid request storms:
  ```dart
  // Using rxdart or a timer-based transformer
  stream.debounceTime(const Duration(milliseconds: 300));
  ```
- **Throttle / Audit**: Emit the first event immediately and ignore subsequent events for a duration. Useful for button debouncing (preventing double taps).

## Ordering and Latest-Wins (SwitchMap Pattern)

- When an asynchronous operation produces an asynchronous result, sequential calls can complete out of order (a slow earlier query finishing after a fast later query).
- Use `switchMap` semantics: map incoming events to a new stream, automatically cancelling the previous inner stream.
- Alternatively, assign an incrementing sequence token to each request and discard responses with a token older than the latest dispatched request.

## Testing Asynchronous Streams

- Use `package:fake_async` to control virtual time deterministically. Avoid `Future.delayed` in unit tests.
- Test edge cases: stream errors, early cancellation before completion, rapid succession of inputs, and unmounting while an asynchronous emission is in flight.
- Hold cleanup of the first listener with a completer, issue two newer queries, and assert neither subscribes until cleanup finishes. After completion, assert only the newest query subscribes. Complete older result work after the newest result and assert it cannot emit. Dispose during pending cleanup and assert that no listener is attached afterward.
- Fail the pending cancellation, assert the owner receives the error, then start a fresh query and verify it can subscribe once the owner has established that retry is safe.
