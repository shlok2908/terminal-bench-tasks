import React, { useEffect, useMemo, useState } from "react";
import TaskDetail from "./components/TaskDetail.jsx";
import TaskList from "./components/TaskList.jsx";

const DIFFICULTY_FILTERS = ["All", "Easy", "Medium"];

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [difficultyFilter, setDifficultyFilter] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function fetchTasks() {
      try {
        setLoading(true);
        const response = await fetch("/api/tasks");
        if (!response.ok) {
          throw new Error(`API returned status ${response.status}`);
        }
        const data = await response.json();
        if (!active) return;

        const loadedTasks = data.tasks ?? [];
        setTasks(loadedTasks);
        if (loadedTasks.length > 0) {
          setSelectedTaskId(loadedTasks[0].id);
        }
        setError("");
      } catch (err) {
        if (!active) return;
        setError(
          `Unable to load tasks from /api/tasks (${err.message}). Make sure the backend server is running.`
        );
      } finally {
        if (active) setLoading(false);
      }
    }

    fetchTasks();
    return () => {
      active = false;
    };
  }, []);

  const filteredTasks = useMemo(() => {
    if (difficultyFilter === "All") return tasks;
    return tasks.filter(
      (task) => task.difficulty.toLowerCase() === difficultyFilter.toLowerCase()
    );
  }, [tasks, difficultyFilter]);

  const selectedTask = useMemo(
    () =>
      filteredTasks.find((task) => task.id === selectedTaskId) ??
      filteredTasks[0] ??
      null,
    [filteredTasks, selectedTaskId]
  );

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <h1>Terminal-Bench Tasks</h1>
          <p className="subtitle">
            Language-driven and outcome-driven Python benchmark tasks with automated graders.
          </p>
        </div>

        <div className="filter-bar" role="group" aria-label="Filter by difficulty">
          {DIFFICULTY_FILTERS.map((level) => (
            <button
              key={level}
              type="button"
              className={`filter-btn ${difficultyFilter === level ? "active" : ""}`}
              onClick={() => setDifficultyFilter(level)}
            >
              {level}
            </button>
          ))}
        </div>
      </header>

      {error && <div className="status-banner">{error}</div>}

      {loading ? (
        <div className="panel">Loading benchmark tasks...</div>
      ) : (
        <div className="layout-grid">
          <TaskList
            tasks={filteredTasks}
            selectedTaskId={selectedTask?.id ?? null}
            onSelectTask={setSelectedTaskId}
          />
          <TaskDetail task={selectedTask} />
        </div>
      )}
    </main>
  );
}
