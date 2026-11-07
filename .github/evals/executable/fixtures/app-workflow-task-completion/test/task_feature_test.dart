import 'dart:async';

import 'package:app_workflow_task_fixture/data/task_repository.dart';
import 'package:app_workflow_task_fixture/model/task.dart';
import 'package:app_workflow_task_fixture/state/task_controller.dart';
import 'package:app_workflow_task_fixture/ui/task_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

const originalTask = Task(
  id: 'task-7',
  title: 'Review invoice',
  completed: false,
);

Map<String, Object?> serverTask({bool completed = true}) => {
  'id': 'task-7',
  'title': 'Invoice reviewed by server',
  'completed': completed,
};

class ControlledApi implements TaskApi {
  final requests = <String>[];
  final pending = <Completer<Map<String, Object?>>>[];

  @override
  Future<Map<String, Object?>> completeTask(String id) {
    requests.add(id);
    final response = Completer<Map<String, Object?>>();
    pending.add(response);
    return response.future;
  }
}

void main() {
  test(
    'repository preserves the confirmed wire fields, including false',
    () async {
      for (final completed in [true, false]) {
        final api = ControlledApi();
        final operation = TaskRepository(api).complete(originalTask.id);
        api.pending.single.complete(serverTask(completed: completed));
        final task = await operation;
        expect(api.requests, ['task-7']);
        expect(task.id, 'task-7');
        expect(task.title, 'Invoice reviewed by server');
        expect(task.completed, completed);
      }
    },
  );

  test(
    'controller announces pending and rejects duplicate submission',
    () async {
      final api = ControlledApi();
      final controller = TaskController(TaskRepository(api), originalTask);
      addTearDown(controller.dispose);
      var notifications = 0;
      controller.addListener(() => notifications++);

      final operation = controller.complete();
      expect(
        controller.saving,
        isTrue,
        reason: 'Pending must precede awaiting IO',
      );
      expect(controller.task, same(originalTask));
      expect(notifications, 1);
      final duplicate = controller.complete();
      expect(api.requests, ['task-7']);

      api.pending.single.complete(serverTask());
      await Future.wait([operation, duplicate]);
      expect(controller.saving, isFalse);
      expect(controller.task.title, 'Invoice reviewed by server');
      expect(controller.task.completed, isTrue);
      expect(controller.error, isNull);
      expect(notifications, 2);
      await controller.complete();
      expect(api.requests, [
        'task-7',
      ], reason: 'Completed tasks cannot resubmit');
    },
  );

  test('controller preserves data on failure and permits retry', () async {
    final api = ControlledApi();
    final controller = TaskController(TaskRepository(api), originalTask);
    addTearDown(controller.dispose);

    final failed = controller.complete();
    api.pending.single.completeError(StateError('offline'));
    await failed;
    expect(controller.task, same(originalTask));
    expect(controller.saving, isFalse);
    expect(controller.error, isNotEmpty);

    final retry = controller.complete();
    expect(controller.error, isNull);
    expect(controller.saving, isTrue);
    expect(api.requests, ['task-7', 'task-7']);
    api.pending.last.complete(serverTask());
    await retry;
    expect(controller.task.completed, isTrue);
  });

  for (final fails in [false, true]) {
    test(
      'disposed controller ignores late ${fails ? 'failure' : 'success'}',
      () async {
        final api = ControlledApi();
        final controller = TaskController(TaskRepository(api), originalTask);
        var notifications = 0;
        controller.addListener(() => notifications++);
        final operation = controller.complete();
        final notificationsBeforeDispose = notifications;
        controller.dispose();
        if (fails) {
          api.pending.single.completeError(StateError('late failure'));
        } else {
          api.pending.single.complete(serverTask());
        }
        await operation;
        expect(controller.task, same(originalTask));
        expect(controller.error, isNull);
        expect(notifications, notificationsBeforeDispose);
        await controller.complete();
        expect(api.requests, ['task-7']);
      },
    );
  }

  testWidgets('UI integrates pending, confirmed data, and completed state', (
    tester,
  ) async {
    final api = ControlledApi();
    final controller = TaskController(TaskRepository(api), originalTask);
    addTearDown(controller.dispose);
    await tester.pumpWidget(
      MaterialApp(home: TaskScreen(controller: controller)),
    );
    expect(find.text('Review invoice'), findsOneWidget);

    await tester.tap(find.text('Complete task'));
    await tester.pump();
    expect(controller.saving, isTrue);
    expect(find.text('Saving…'), findsOneWidget);
    expect(
      tester.widget<FilledButton>(find.byType(FilledButton)).onPressed,
      isNull,
    );
    expect(api.requests, ['task-7']);
    expect(find.text('Invoice reviewed by server'), findsNothing);

    api.pending.single.complete(serverTask());
    await tester.pumpAndSettle();
    expect(find.text('Invoice reviewed by server'), findsOneWidget);
    expect(find.text('Completed'), findsOneWidget);
    expect(
      tester.widget<FilledButton>(find.byType(FilledButton)).onPressed,
      isNull,
    );
    expect(tester.takeException(), isNull);
  });

  testWidgets(
    'UI shows a recoverable error and retries through the repository',
    (tester) async {
      final api = ControlledApi();
      final controller = TaskController(TaskRepository(api), originalTask);
      addTearDown(controller.dispose);
      await tester.pumpWidget(
        MaterialApp(home: TaskScreen(controller: controller)),
      );
      await tester.tap(find.text('Complete task'));
      await tester.pump();
      api.pending.single.completeError(StateError('offline'));
      await tester.pumpAndSettle();

      expect(controller.error, isNotEmpty);
      expect(find.text(controller.error!), findsOneWidget);
      expect(find.text('Review invoice'), findsOneWidget);
      expect(
        tester.widget<FilledButton>(find.byType(FilledButton)).onPressed,
        isNotNull,
      );
      await tester.tap(find.byType(FilledButton));
      await tester.pump();
      expect(api.requests, ['task-7', 'task-7']);
      expect(controller.error, isNull);
      api.pending.last.complete(serverTask());
      await tester.pumpAndSettle();
      expect(find.text('Completed'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );
}
