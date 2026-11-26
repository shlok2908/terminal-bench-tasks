# Terminal-Bench Tasks – Benchmark & Sample Application

A benchmark project containing two Terminal-Bench-inspired Python programming tasks, automated `pytest` graders, isolated Docker environments, and a Node.js + React sample web application for viewing task details.

## Tasks Overview

| Task ID | Task Name | Task Type | Difficulty |
|---|---|---|---|
| TASK-001 | Fix Number Statistics Program | Language-driven | Easy |
| TASK-002 | Improve Task Tracking Results | Outcome-driven | Medium |

## Repository Structure

```text
.
├── tasks/
│   ├── task-001-number-statistics/
│   │   ├── statement.md
│   │   ├── environment/Dockerfile
│   │   ├── src/statistics.py
│   │   ├── solution/statistics.py
│   │   └── grader/test_task.py
│   └── task-002-task-tracker/
│       ├── statement.md
│       ├── environment/Dockerfile
│       ├── src/task_tracker.py
│       ├── solution/task_tracker.py
│       └── grader/test_task.py
├── backend/
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── vite.config.js
│   └── src/
├── docker-compose.yml
├── README.md
└── NOTES.md
```

Note: Both `src/` files now contain the verified fixed implementations so the graders pass directly out of the box (reference copies are also kept in each task's `solution/` directory).

## Running the Graders

Install `pytest` if needed:

```bash
pip install pytest
```

Run Task 1 grader:

```bash
pytest tasks/task-001-number-statistics/grader/ -v
```

Run Task 2 grader:

```bash
pytest tasks/task-002-task-tracker/grader/ -v
```

Run all graders together:

```bash
pytest -v
```

## Docker Environment

Build Docker images from the repository root:

```bash
docker build -t task-001 -f tasks/task-001-number-statistics/environment/Dockerfile .
docker build -t task-002 -f tasks/task-002-task-tracker/environment/Dockerfile .
```

Run the containers:

```bash
docker run --rm task-001
docker run --rm task-002
```

Or use Docker Compose:

```bash
docker compose build
docker compose run --rm task-001
docker compose run --rm task-002
```

## Full-Stack Sample Application

Start the Express backend (serves `GET /api/tasks` on port `3001`):

```bash
cd backend
npm install
npm start
```

Start the React + Vite frontend in a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (typically `http://localhost:5173`).
