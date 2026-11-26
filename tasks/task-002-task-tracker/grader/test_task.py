"""Automated grader for TASK-002: Improve Task Tracking Results."""

import importlib.util
import os
from pathlib import Path
import random

TASK_DIR = Path(__file__).resolve().parent.parent
TARGET_FILE = Path(os.environ.get("TASK_002_SRC", TASK_DIR / "src" / "task_tracker.py"))


def _load_module():
    spec = importlib.util.spec_from_file_location("task002_tracker", TARGET_FILE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tracker_mod = _load_module()
TaskTracker = tracker_mod.TaskTracker


def test_independent_instances_and_empty_collection():
    t1 = TaskTracker()
    t2 = TaskTracker()

    assert t1.get_all_tasks() == []
    assert t1.get_completed_tasks() == []
    assert t1.get_pending_tasks() == []
    assert t1.get_counts() == {"total": 0, "completed": 0, "pending": 0}

    summary = t1.get_summary()
    assert summary["total"] == 0
    assert summary["completed"] == 0
    assert summary["pending"] == 0
    assert summary["completion_rate"] == 0
    assert summary["completed_tasks"] == []
    assert summary["pending_tasks"] == []

    formatted = t1.format_summary()
    assert "Total tasks: 0" in formatted
    assert "Completed: 0" in formatted
    assert "Pending: 0" in formatted

    t1.add_task("Only in t1", task_id="A1")
    assert t2.get_all_tasks() == []


def test_distinguish_completed_and_pending_accurately():
    initial = [
        {"id": "1", "title": "Setup repo", "completed": True},
        {"id": "2", "title": "Write tests", "completed": False},
        {"id": "3", "title": "Review docs"},  # missing completed defaults to pending
    ]
    snapshot = [dict(item) for item in initial]
    tracker = TaskTracker(initial)
    assert initial == snapshot

    completed = tracker.get_completed_tasks()
    pending = tracker.get_pending_tasks()
    assert [t["id"] for t in completed] == ["1"]
    assert [t["id"] for t in pending] == ["2", "3"]
    assert tracker.get_counts() == {"total": 3, "completed": 1, "pending": 2}


def test_state_transitions_preserve_task_information():
    tracker = TaskTracker()
    tracker.add_task("Draft specification", completed=False, task_id="T-10")
    tracker.add_task("Build Docker image", completed=False, task_id="T-20")

    assert tracker.complete_task("T-10") is True
    assert tracker.complete_task("MISSING") is False

    completed = tracker.get_completed_tasks()
    pending = tracker.get_pending_tasks()
    assert len(completed) == 1
    assert completed[0]["id"] == "T-10"
    assert completed[0]["title"] == "Draft specification"
    assert completed[0]["completed"] is True

    assert len(pending) == 1
    assert pending[0]["id"] == "T-20"
    assert pending[0]["title"] == "Build Docker image"

    assert tracker.reopen_task("T-10") is True
    assert tracker.get_counts() == {"total": 2, "completed": 0, "pending": 2}


def test_no_duplicate_tasks_or_duplicate_summary_entries():
    tracker = TaskTracker()
    tracker.add_task("First task", completed=False, task_id="DUP-1")
    tracker.add_task("First task updated", completed=True, task_id="DUP-1")
    tracker.add_task("Second task", completed=False, task_id="UNIQ-2")

    all_tasks = tracker.get_all_tasks()
    ids = [t["id"] for t in all_tasks]
    assert len(ids) == len(set(ids)) == 2
    assert tracker.get_counts() == {"total": 2, "completed": 1, "pending": 1}

    formatted = tracker.format_summary()
    assert formatted.count("DUP-1") == 1
    assert formatted.count("UNIQ-2") == 1
    assert "First task updated" in formatted


def test_summary_matches_collection_across_varied_inputs():
    rng = random.Random(4242)
    for trial in range(15):
        tracker = TaskTracker()
        expected_completed = 0
        expected_pending = 0
        count = rng.randint(1, 12)
        for idx in range(count):
            is_done = rng.choice([True, False])
            title = f"Trial {trial} Task {idx}"
            tracker.add_task(title, completed=is_done, task_id=f"id-{trial}-{idx}")
            if is_done:
                expected_completed += 1
            else:
                expected_pending += 1

        summary = tracker.get_summary()
        assert summary["total"] == count
        assert summary["completed"] == expected_completed
        assert summary["pending"] == expected_pending
        assert len(summary["completed_tasks"]) == expected_completed
        assert len(summary["pending_tasks"]) == expected_pending
        completed_ids = {t["id"] for t in summary["completed_tasks"]}
        pending_ids = {t["id"] for t in summary["pending_tasks"]}
        assert completed_ids.isdisjoint(pending_ids)
        assert len(completed_ids | pending_ids) == count
