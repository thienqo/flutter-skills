import 'package:flutter/foundation.dart';

import '../data/task_repository.dart';
import '../model/task.dart';

class TaskController extends ChangeNotifier {
  TaskController(this.repository, this.task);

  final TaskRepository repository;
  Task task;
  bool saving = false;
  String? error;
  bool _disposed = false;

  Future<void> complete() async {
    if (_disposed || saving || task.completed) return;
    saving = true;
    error = null;
    notifyListeners();
    try {
      final confirmed = await repository.complete(task.id);
      if (_disposed) return;
      task = confirmed;
    } catch (_) {
      if (_disposed) return;
      error = 'Unable to complete task. Please retry.';
    } finally {
      if (!_disposed) {
        saving = false;
        notifyListeners();
      }
    }
  }

  @override
  void dispose() {
    _disposed = true;
    super.dispose();
  }
}
