// A fake store and journal that survive recreation of the purchase processor.
class Journal {
  final verified = <String>{};
  final delivered = <String>{};
  int coins = 0;

  void grant(String token) {
    if (delivered.add(token)) coins += 10;
  }
}

class Interrupted implements Exception {}

class FakeStore {
  final consumed = <String>{};
  final finished = <String>{};
  bool loseNextConsumeResponse = false;
  bool interruptBeforeFinish = false;

  void consume(String token, Journal journal) {
    check(journal.verified.contains(token), 'consume without a saved identity');
    consumed.add(token);
    if (loseNextConsumeResponse) {
      loseNextConsumeResponse = false;
      throw Interrupted();
    }
  }

  void finish(String token, Journal journal) {
    check(journal.delivered.contains(token), 'finish before delivery');
    if (interruptBeforeFinish) {
      interruptBeforeFinish = false;
      throw Interrupted();
    }
    finished.add(token);
  }
}

class Processor {
  Processor(this.journal, this.store);

  final Journal journal;
  final FakeStore store;

  void play(String token, {required bool consumeFirst}) {
    check(journal.verified.contains(token), 'unverified Play purchase');
    if (!consumeFirst) journal.grant(token);
    if (!store.consumed.contains(token)) store.consume(token, journal);
    if (consumeFirst && store.consumed.contains(token)) journal.grant(token);
  }

  void apple(String token) {
    check(journal.verified.contains(token), 'unverified StoreKit purchase');
    journal.grant(token);
    if (!store.finished.contains(token)) store.finish(token, journal);
  }
}

void check(bool condition, String message) {
  if (!condition) throw StateError(message);
}

void expectInterruption(void Function() process) {
  try {
    process();
  } on Interrupted {
    return;
  }
  throw StateError('expected an interruption');
}

void main() {
  const token = 'verified-transaction';
  for (final consumeFirst in [true, false]) {
    final journal = Journal()..verified.add(token);
    final store = FakeStore()..loseNextConsumeResponse = true;
    expectInterruption(
      () => Processor(journal, store).play(token, consumeFirst: consumeFirst),
    );
    check(journal.coins == (consumeFirst ? 0 : 10), 'wrong Play order');
    check(store.consumed.contains(token), 'fake consume did not succeed');

    final restarted = Processor(journal, store);
    for (final saved in journal.verified) {
      restarted.play(saved, consumeFirst: consumeFirst);
    }
    restarted.play(token, consumeFirst: consumeFirst);
    check(journal.coins == 10, 'Play purchase lost or credited twice');
    print(
      'Play ${consumeFirst ? 'consume-first' : 'grant-first'} recovery passed',
    );
  }

  final journal = Journal()..verified.add(token);
  final store = FakeStore()..interruptBeforeFinish = true;
  expectInterruption(() => Processor(journal, store).apple(token));
  check(journal.coins == 10 && store.finished.isEmpty, 'wrong StoreKit order');

  final restarted = Processor(journal, store);
  restarted.apple(token);
  restarted.apple(token);
  check(
    journal.coins == 10 && store.finished.contains(token),
    'StoreKit recovery failed',
  );
  print('StoreKit delivery-before-finish recovery passed');
}
