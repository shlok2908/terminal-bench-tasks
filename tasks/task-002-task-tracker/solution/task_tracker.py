"""Reference solution for TASK-002 (Improve Task Tracking Results)."""

from copy import deepcopy
from typing import Any


def _normalize_completed(value: Any) -> bool:
    """Normalize completed flag to a strict boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "done", "completed"}
    return bool(value)


class TaskTracker:
    """Manage a collection of unique tasks and generate accurate summaries."""

    def __init__(self, tasks: list[dict[str, Any]] | None = None) -> None:
        self._tasks: list[dict[str, Any]] = []
        self._seen_ids: set[str | int] = set()
        self._next_auto_id = 1

        if tasks:
            for raw_task in tasks:
                if not isinstance(raw_task, dict):
                    continue
                task_id = raw_task.get("id")
                title = str(raw_task.get("title", "")).strip() or "Untitled"
                completed = _normalize_completed(raw_task.get("completed", False))
                extra = {
                    k: v
                    for k, v in raw_task.items()
                    if k not in {"id", "title", "completed"}
                }
                self.add_task(title=title, completed=completed, task_id=task_id, **extra)

    def _generate_unique_id(self) -> str:
        """Generate a unique task identifier that does not collide with existing IDs."""
        while f"task-{self._next_auto_id}" in self._seen_ids:
            self._next_auto_id += 1
        generated = f"task-{self._next_auto_id}"
        self._next_auto_id += 1
        return generated

    def add_task(
        self,
        title: str,
        completed: bool = False,
        task_id: str | int | None = None,
        **metadata: Any,
    ) -> dict[str, Any]:
        """Add a unique task or update/deduplicate cleanly without losing existing tasks."""
        resolved_id = self._generate_unique_id() if task_id is None else task_id
        clean_title = str(title).strip() or "Untitled"
        is_completed = _normalize_completed(completed)

        if resolved_id in self._seen_ids:
            for existing in self._tasks:
                if existing["id"] == resolved_id:
                    existing["title"] = clean_title
                    existing["completed"] = is_completed
                    existing.update(metadata)
                    return deepcopy(existing)

        task: dict[str, Any] = {
            **metadata,
            "id": resolved_id,
            "title": clean_title,
            "completed": is_completed,
        }
        self._tasks.append(task)
        self._seen_ids.add(resolved_id)
        return deepcopy(task)

    def complete_task(self, task_id: str | int) -> bool:
        """Mark the matching task as completed while preserving all task info."""
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return True
        return False

    def reopen_task(self, task_id: str | int) -> bool:
        """Mark the matching task as pending while preserving all task info."""
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = False
                return True
        return False

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Return copies of all tracked tasks."""
        return [deepcopy(task) for task in self._tasks]

    def get_completed_tasks(self) -> list[dict[str, Any]]:
        """Return copies of all completed tasks."""
        return [deepcopy(task) for task in self._tasks if task["completed"] is True]

    def get_pending_tasks(self) -> list[dict[str, Any]]:
        """Return copies of all pending tasks."""
        return [deepcopy(task) for task in self._tasks if task["completed"] is False]

    def get_counts(self) -> dict[str, int]:
        """Return total, completed, and pending task counts."""
        total = len(self._tasks)
        completed = sum(1 for task in self._tasks if task["completed"] is True)
        pending = total - completed
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
        }

    def get_summary(self) -> dict[str, Any]:
        """Return a structured summary matching the current task collection."""
        counts = self.get_counts()
        completed_tasks = self.get_completed_tasks()
        pending_tasks = self.get_pending_tasks()
        completion_rate = (
            0.0
            if counts["total"] == 0
            else round((counts["completed"] / counts["total"]) * 100, 2)
        )
        return {
            "total": counts["total"],
            "completed": counts["completed"],
            "pending": counts["pending"],
            "completion_rate": completion_rate,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
        }

    def format_summary(self) -> str:
        """Return an accurate human-readable summary of all tasks."""
        summary = self.get_summary()
        lines = [
            f"Total tasks: {summary['total']}",
            f"Completed: {summary['completed']}",
            f"Pending: {summary['pending']}",
            f"Completion rate: {summary['completion_rate']}%",
        ]
        if summary["total"] == 0:
            lines.append("No tasks available.")
            return "\n".join(lines)

        lines.append("Completed tasks:")
        if summary["completed_tasks"]:
            for task in summary["completed_tasks"]:
                lines.append(f"  - [x] {task['title']} ({task['id']})")
        else:
            lines.append("  (none)")

        lines.append("Pending tasks:")
        if summary["pending_tasks"]:
            for task in summary["pending_tasks"]:
                lines.append(f"  - [ ] {task['title']} ({task['id']})")
        else:
            lines.append("  (none)")

        return "\n".join(lines)


def main() -> None:
    """Demonstrate basic task tracker usage."""
    tracker = TaskTracker()
    tracker.add_task("Write unit tests", completed=True, task_id="T1")
    tracker.add_task("Fix bug in summary", completed=False, task_id="T2")
    print(tracker.format_summary())


if __name__ == "__main__":
    main()
