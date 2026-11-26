# Task 2 – Improve Task Tracking Results

## Task Information

- **Task ID:** TASK-002
- **Task Name:** Improve Task Tracking Results
- **Type:** Outcome-driven
- **Language:** Python
- **Difficulty:** Medium

## Statement

A small task-tracking application (`src/task_tracker.py`) is available, but its results are not always reliable.

Improve the application so that users can depend on its task information.

After the improvements, the application should:

- Maintain accurate task information.
- Correctly distinguish completed and pending tasks.
- Display the correct number of completed and pending tasks.
- Provide accurate summaries of the current tasks.
- Handle situations where no tasks are available.
- Avoid displaying incorrect or duplicated task information.

The final application should behave consistently across different task collections and should not lose existing task information during normal operations.

You are free to investigate the existing project and determine the necessary changes. The final result will be evaluated based on its behavior rather than the implementation approach.

## Environment

- Python 3.11 or later.
- Linux-based environment.
- Terminal access.
- Existing task-tracking application source code (`src/task_tracker.py`).
- No external Python packages required.

## Difficulty Note

This is a medium-level task because the expected outcome is described without specifying which functions or files need modification.

The agent must understand the existing application, identify incorrect behavior, determine the necessary changes, and verify that the final results are accurate.

## Grading Criteria

The grader will verify:

1. Task information is maintained correctly.
2. Completed tasks are identified accurately.
3. Pending tasks are identified accurately.
4. Task counts are correct.
5. Summary information matches the actual task collection.
6. Empty task collections are handled correctly.
7. Duplicate or incorrect task information is not introduced.
8. Existing functionality continues to work.
