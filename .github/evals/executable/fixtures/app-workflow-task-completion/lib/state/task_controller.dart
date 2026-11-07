import 'package:flutter/foundation.dart';

import '../data/task_repository.dart';
import '../model/task.dart';

class TaskController extends ChangeNotifier {
  TaskController(this.repository, this.task);

  final TaskRepository repository;
  Task task;
  bool saving = false;
  String? error;

  Future<void> complete() async {
    task = await repository.complete(task.id);
    notifyListeners();
  }
}
