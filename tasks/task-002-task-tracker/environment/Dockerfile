FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest

COPY tasks/task-002-task-tracker/statement.md /app/statement.md
COPY tasks/task-002-task-tracker/src/ /app/src/
COPY tasks/task-002-task-tracker/grader/ /app/grader/

CMD ["pytest", "grader/", "-v"]
