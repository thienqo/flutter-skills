import 'dart:async';

import '../lib/media_source_owner.dart';

class FakeHandle implements MediaHandle {
  FakeHandle(this.name, {this.failClose = false});

  final String name;
  final bool failClose;
  int closes = 0;

  @override
  Future<void> close() async {
    closes++;
    if (closes > 1) throw StateError('Duplicate close: $name');
    if (failClose) throw StateError('Close failed: $name');
  }
}

void require(bool condition, String message) {
  if (!condition) throw StateError(message);
}

Future<void> reversedCompletion() async {
  final owner = MediaSourceOwner();
  final a = Completer<MediaHandle>();
  final b = Completer<MediaHandle>();
  final older = owner.start(() => a.future);
  final newer = owner.start(() => b.future);
  final second = FakeHandle('B');
  b.complete(second);
  await newer;
  final first = FakeHandle('A');
  a.complete(first);
  await older;
  require(identical(owner.current, second), 'Stale source replaced latest');
  require(first.closes == 1, 'Stale successful handle was not released');
  require(second.closes == 0, 'Current source was prematurely released');
  await owner.dispose();
  require(second.closes == 1, 'Current source leaked on disposal');
}

Future<void> stopDuringOpen() async {
  final owner = MediaSourceOwner();
  final pending = Completer<MediaHandle>();
  final operation = owner.start(() => pending.future);
  await owner.stop();
  final handle = FakeHandle('late');
  pending.complete(handle);
  await operation;
  require(owner.current == null, 'Stopped owner revived from pending open');
  require(handle.closes == 1, 'Late successful handle leaked after stop');
  await owner.dispose();
}

Future<void> disposal() async {
  final owner = MediaSourceOwner();
  final pending = Completer<MediaHandle>();
  final operation = owner.start(() => pending.future);
  await owner.dispose();
  final handle = FakeHandle('late-disposed');
  pending.complete(handle);
  await operation;
  require(owner.current == null, 'Disposed owner revived');
  require(handle.closes == 1, 'Disposed pending handle leaked');
  var opens = 0;
  await owner.start(() async {
    opens++;
    return FakeHandle('must-not-open');
  });
  require(opens == 0, 'Disposed owner acquired another source');
  await owner.dispose();
}

Future<void> replacementAndRepeatedStop() async {
  final owner = MediaSourceOwner();
  final first = FakeHandle('first');
  final second = FakeHandle('second');
  await owner.start(() async => first);
  await owner.start(() async => second);
  require(first.closes == 1, 'Replaced active handle leaked');
  require(identical(owner.current, second), 'Replacement was not adopted');
  await Future.wait([owner.stop(), owner.stop()]);
  require(second.closes == 1, 'Concurrent stop closed a handle twice');
  require(owner.current == null, 'Stop kept a released handle');
  await owner.dispose();
}

Future<void> failedReplacement() async {
  final owner = MediaSourceOwner();
  final original = FakeHandle('working');
  await owner.start(() async => original);
  var observed = false;
  try {
    await owner.start(() async => throw StateError('source failed'));
  } on StateError {
    observed = true;
  }
  require(observed, 'Initialization failure was swallowed');
  require(identical(owner.current, original), 'Failure lost working source');
  require(original.closes == 0, 'Failed replacement released working source');
  await owner.dispose();
}

Future<void> failedClose() async {
  final owner = MediaSourceOwner();
  final handle = FakeHandle('failure', failClose: true);
  await owner.start(() async => handle);
  var observed = false;
  try {
    await owner.stop();
  } on StateError {
    observed = true;
  }
  require(observed, 'Cleanup failure was swallowed');
  require(owner.current == null, 'Failed close left handle current');
  await owner.stop();
  require(handle.closes == 1, 'Failed close was retried implicitly');
  await owner.dispose();
}

Future<void> main() async {
  final checks = <String, Future<void> Function()>{
    'reversed completion': reversedCompletion,
    'stop during open': stopDuringOpen,
    'disposal': disposal,
    'replacement and concurrent stop': replacementAndRepeatedStop,
    'failed replacement': failedReplacement,
    'failed close': failedClose,
  };
  for (final entry in checks.entries) {
    await entry.value();
    print('PASS ${entry.key}');
  }
}
