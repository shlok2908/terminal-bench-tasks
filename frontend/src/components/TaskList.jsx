import React from "react";

function difficultyClass(difficulty) {
  return difficulty?.toLowerCase() === "easy" ? "badge-easy" : "badge-medium";
}

export default function TaskList({ tasks, selectedTaskId, onSelectTask }) {
  return (
    <aside className="panel">
      <h2 className="panel-title">Benchmark Tasks ({tasks.length})</h2>
      {tasks.length === 0 ? (
        <p className="subtitle">No tasks match the active filter.</p>
      ) : (
        <div className="task-list">
          {tasks.map((task) => {
            const isSelected = task.id === selectedTaskId;
            return (
              <button
                key={task.id}
                type="button"
                className={`task-card ${isSelected ? "selected" : ""}`}
                onClick={() => onSelectTask(task.id)}
              >
                <div className="task-card-top">
                  <span className="task-id">{task.id}</span>
                  <span className={`badge ${difficultyClass(task.difficulty)}`}>
                    {task.difficulty}
                  </span>
                </div>
                <h3 className="task-name">{task.name}</h3>
                <div className="badge-row">
                  <span className="badge badge-type">{task.type}</span>
                  <span className="badge badge-type">{task.language}</span>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </aside>
  );
}
