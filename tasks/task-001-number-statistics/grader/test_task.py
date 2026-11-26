"""Automated grader for TASK-001: Fix Number Statistics Program."""

import importlib.util
import math
import os
from pathlib import Path
import random

import pytest

TASK_DIR = Path(__file__).resolve().parent.parent
TARGET_FILE = Path(os.environ.get("TASK_001_SRC", TASK_DIR / "src" / "statistics.py"))


def _load_module():
    spec = importlib.util.spec_from_file_location("task001_statistics", TARGET_FILE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stats_mod = _load_module()


def test_standard_positive_lists():
    res1 = stats_mod.calculate_statistics([10, 20, 30])
    assert res1["count"] == 3
    assert res1["sum"] == 60
    assert res1["average"] == pytest.approx(20)
    assert res1["min"] == 10
    assert res1["max"] == 30

    res2 = stats_mod.calculate_statistics([5, 15])
    assert res2["count"] == 2
    assert res2["sum"] == 20
    assert res2["average"] == pytest.approx(10)
    assert res2["min"] == 5
    assert res2["max"] == 15


def test_negative_and_zero_values():
    res = stats_mod.calculate_statistics([-5, 0, 5])
    assert res["count"] == 3
    assert res["sum"] == 0
    assert res["average"] == pytest.approx(0)
    assert res["min"] == -5
    assert res["max"] == 5

    all_neg = stats_mod.calculate_statistics([-10, -25, -4])
    assert all_neg["count"] == 3
    assert all_neg["sum"] == -39
    assert all_neg["average"] == pytest.approx(-13)
    assert all_neg["min"] == -25
    assert all_neg["max"] == -4


def test_empty_and_none_input():
    for empty in ([], None):
        res = stats_mod.calculate_statistics(empty)
        assert res["count"] == 0
        assert res["sum"] == 0
        assert res["average"] is None
        assert res["min"] is None
        assert res["max"] is None


def test_invalid_values_ignored():
    res = stats_mod.calculate_statistics([10, "abc", 20])
    assert res["count"] == 2
    assert res["sum"] == 30
    assert res["average"] == pytest.approx(15)
    assert res["min"] == 10
    assert res["max"] == 20

    mixed = [None, "bad", True, False, {"x": 1}, [2], float("nan"), float("inf"), 4, 8.5]
    res_mixed = stats_mod.calculate_statistics(mixed)
    assert res_mixed["count"] == 2
    assert res_mixed["sum"] == pytest.approx(12.5)
    assert res_mixed["average"] == pytest.approx(6.25)
    assert res_mixed["min"] == 4
    assert res_mixed["max"] == 8.5


def test_all_invalid_values():
    res = stats_mod.calculate_statistics(["abc", None, True, []])
    assert res["count"] == 0
    assert res["sum"] == 0
    assert res["average"] is None
    assert res["min"] is None
    assert res["max"] is None


def test_input_not_mutated_and_format_works():
    data = [10, "abc", 20]
    snapshot = list(data)
    res = stats_mod.calculate_statistics(data)
    assert data == snapshot

    formatted = stats_mod.format_statistics(res)
    assert "Count: 2" in formatted
    assert "Sum: 30" in formatted
    assert "Average: 15" in formatted

    empty_formatted = stats_mod.format_statistics(stats_mod.calculate_statistics([]))
    assert "Count: 0" in empty_formatted


def test_randomized_unseen_inputs_prevent_hardcoding():
    rng = random.Random(20261125)
    for _ in range(25):
        valid_nums = [round(rng.uniform(-100, 100), 2) for _ in range(rng.randint(1, 15))]
        noise = ["err", None, True, False, object()]
        combined = valid_nums + rng.sample(noise, k=rng.randint(0, len(noise)))
        rng.shuffle(combined)

        res = stats_mod.calculate_statistics(combined)
        expected_sum = sum(valid_nums)
        assert res["count"] == len(valid_nums)
        assert res["sum"] == pytest.approx(expected_sum)
        assert res["average"] == pytest.approx(expected_sum / len(valid_nums))
        assert res["min"] == pytest.approx(min(valid_nums))
        assert res["max"] == pytest.approx(max(valid_nums))
        assert math.isfinite(res["average"])
