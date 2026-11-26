FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest

COPY tasks/task-001-number-statistics/statement.md /app/statement.md
COPY tasks/task-001-number-statistics/src/ /app/src/
COPY tasks/task-001-number-statistics/grader/ /app/grader/

CMD ["pytest", "grader/", "-v"]
