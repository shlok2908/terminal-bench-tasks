# Task 1 – Fix Number Statistics Program

## Task Information

- **Task ID:** TASK-001
- **Task Name:** Fix Number Statistics Program
- **Type:** Language-driven
- **Language:** Python
- **Difficulty:** Easy

## Statement

You are given an existing Python program (`src/statistics.py`) that calculates basic statistics from a list of numbers.

The current implementation does not handle all input cases correctly. Your task is to inspect the existing program, identify the issues, and fix its behavior.

The program should correctly calculate:

- Total number of valid numeric values (`count`).
- Sum of all valid values (`sum`).
- Average of the values (`average`).
- Minimum value (`min`).
- Maximum value (`max`).

The program must also handle empty input and invalid values without crashing.

Do not remove existing functionality (`calculate_statistics`, `format_statistics`, and `main`). Make sure the program produces accurate results for normal inputs and edge cases.

## Environment

- Python 3.11 or later.
- Linux-based environment.
- Terminal access.
- No external Python packages required for `src/statistics.py`.

## Difficulty Note

This is an easy-level task because it involves understanding an existing Python program, identifying logical errors, handling edge cases, and validating the output.

The main challenges include handling empty input, invalid values (such as strings, `None`, booleans, or non-finite floats), and calculating statistics accurately (including negative numbers).

## Expected Behavior

| Input | Expected Result |
|---|---|
| `[10, 20, 30]` | Count: 3, Sum: 60, Average: 20, Min: 10, Max: 30 |
| `[5, 15]` | Count: 2, Sum: 20, Average: 10, Min: 5, Max: 15 |
| `[]` | No crash; `count=0`, `sum=0`, `average=None`, `min=None`, `max=None` |
| `[10, "abc", 20]` | Ignore `"abc"` -> Count: 2, Sum: 30, Average: 15, Min: 10, Max: 20 |
| `[-5, 0, 5]` | Count: 3, Sum: 0, Average: 0, Min: -5, Max: 5 |

## Grading Criteria

The grader will verify:

1. Correct count of valid numbers.
2. Correct sum and average.
3. Correct minimum and maximum values.
4. Proper handling of empty input.
5. Proper handling of invalid values.
6. No unexpected crashes.
