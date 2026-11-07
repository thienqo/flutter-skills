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
              FilledButton(
                onPressed: controller.complete,
                child: const Text('Complete task'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
