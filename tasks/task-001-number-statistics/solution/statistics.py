"""Reference solution for TASK-001 (Number Statistics Program)."""

import math
from typing import Any


def _is_valid_number(value: Any) -> bool:
    """Return True if value is a finite int or float (excluding bool)."""
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


def calculate_statistics(numbers: list[Any] | None) -> dict[str, int | float | None]:
    """Calculate count, sum, average, min, and max for a list of numbers.

    Returns a dictionary with keys:
    - ``count``: total number of valid numeric values (excluding booleans)
    - ``sum``: sum of valid numeric values (0 when no valid values exist)
    - ``average``: arithmetic mean of valid values (None when count is 0)
    - ``min``: smallest valid value (None when count is 0)
    - ``max``: largest valid value (None when count is 0)
    """
    if not numbers:
        return {
            "count": 0,
            "sum": 0,
            "average": None,
            "min": None,
            "max": None,
        }

    valid = [value for value in numbers if _is_valid_number(value)]
    if not valid:
        return {
            "count": 0,
            "sum": 0,
            "average": None,
            "min": None,
            "max": None,
        }

    total = sum(valid)
    count = len(valid)
    return {
        "count": count,
        "sum": total,
        "average": total / count,
        "min": min(valid),
        "max": max(valid),
    }


def format_statistics(stats: dict[str, int | float | None]) -> str:
    """Format a statistics dictionary into a human-readable summary string."""
    avg_text = "N/A" if stats["average"] is None else f"{stats['average']:g}"
    min_text = "N/A" if stats["min"] is None else f"{stats['min']:g}"
    max_text = "N/A" if stats["max"] is None else f"{stats['max']:g}"
    sum_text = f"{stats['sum']:g}"
    return (
        f"Count: {stats['count']}, "
        f"Sum: {sum_text}, "
        f"Average: {avg_text}, "
        f"Min: {min_text}, "
        f"Max: {max_text}"
    )


def main() -> None:
    """Run sample statistics calculations."""
    samples = [
        [10, 20, 30],
        [5, 15],
        [],
        [10, "abc", 20],
        [-5, 0, 5],
    ]
    for sample in samples:
        stats = calculate_statistics(sample)
        print(f"{sample} -> {format_statistics(stats)}")


if __name__ == "__main__":
    main()
