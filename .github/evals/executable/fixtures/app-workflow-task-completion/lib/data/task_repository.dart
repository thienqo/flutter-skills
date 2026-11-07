import '../model/task.dart';

abstract interface class TaskApi {
  Future<Map<String, Object?>> completeTask(String id);
}

class TaskRepository {
  TaskRepository(this.api);

  final TaskApi api;

  Future<Task> complete(String id) async {
    await api.completeTask(id);
    return Task(id: id, title: 'Task', completed: true);
  }
}
