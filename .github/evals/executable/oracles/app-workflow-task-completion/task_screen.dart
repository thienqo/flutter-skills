import 'package:flutter/material.dart';

import '../state/task_controller.dart';

class TaskScreen extends StatelessWidget {
  const TaskScreen({super.key, required this.controller});

  final TaskController controller;

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: controller,
      builder: (context, child) => Scaffold(
        body: SafeArea(
          child: Column(
            children: [
              Text(controller.task.title),
              if (controller.error != null) Text(controller.error!),
              FilledButton(
                onPressed: controller.saving || controller.task.completed
                    ? null
                    : controller.complete,
                child: Text(
                  controller.saving
                      ? 'Saving…'
                      : controller.task.completed
                      ? 'Completed'
                      : 'Complete task',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
