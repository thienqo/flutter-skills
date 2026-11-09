import 'dart:async';

import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

part 'riverpod_guard.dart';

typedef Submit = Future<void> Function(Future<int> result);

class ScreenHarness {
  final container = ProviderContainer();
  final published = <Object>[];
  int disposals = 0;
  late Submit submit;

  late final request = Provider.autoDispose<Submit>((ref) {
    ref.onDispose(() => disposals++);
    final isCurrent = captureLifetime(ref);
    return (result) async {
      try {
        final value = await result;
        if (isCurrent()) published.add(value);
      } catch (error) {
        if (isCurrent()) published.add(error);
      }
    };
  });

  Widget screen({required bool visible}) => UncontrolledProviderScope(
    container: container,
    child: visible
        ? Consumer(
            builder: (context, ref, child) {
              submit = ref.watch(request);
              return const SizedBox();
            },
          )
        : const SizedBox(),
  );
}

void main() {
  for (final fail in [false, true]) {
    testWidgets(
      'remove watching screen before late ${fail ? 'error' : 'success'}',
      (tester) async {
        final harness = ScreenHarness();
        addTearDown(harness.container.dispose);
        await tester.pumpWidget(harness.screen(visible: true));
        await harness.submit(Future.value(1));

        final pending = Completer<int>();
        final completion = harness.submit(pending.future);
        await tester.pumpWidget(harness.screen(visible: false));
        await tester.pumpAndSettle();
        expect(harness.disposals, 1);

        if (fail) {
          pending.completeError(StateError('late error'));
        } else {
          pending.complete(2);
        }
        await completion;
        expect(harness.published, [1]);
        expect(tester.takeException(), isNull);
      },
    );
  }

  testWidgets('a rebuilt provider rejects its old completion', (tester) async {
    final harness = ScreenHarness();
    addTearDown(harness.container.dispose);
    await tester.pumpWidget(harness.screen(visible: true));
    final old = Completer<int>();
    final completion = harness.submit(old.future);

    final current = harness.container.refresh(harness.request);
    await tester.pump();
    expect(harness.disposals, 1);
    await current(Future.value(2));
    old.complete(1);
    await completion;

    expect(harness.published, [2]);
    await tester.pumpWidget(harness.screen(visible: false));
  });
}
