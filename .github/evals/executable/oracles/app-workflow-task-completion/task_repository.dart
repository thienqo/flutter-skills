import '../model/task.dart';

abstract interface class TaskApi {
  Future<Map<String, Object?>> completeTask(String id);
}

class TaskRepository {
  TaskRepository(this.api);

  final TaskApi api;

  Future<Task> complete(String id) async {
    final response = await api.completeTask(id);
    return Task(
      id: response['id'] as String,
      title: response['title'] as String,
      completed: response['completed'] as bool,
    );
  }
}
