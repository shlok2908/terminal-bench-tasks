import React from "react";

export default function TaskDetail({ task }) {
  if (!task) {
    return (
      <section className="panel">
        <p className="subtitle">Select a task to view its statement and environment.</p>
      </section>
    );
  }

  const difficultyClass =
    task.difficulty?.toLowerCase() === "easy" ? "badge-easy" : "badge-medium";
  const imageTag = task.id.toLowerCase();

  return (
    <section className="panel">
      <div className="detail-header">
        <span className="task-id">{task.id}</span>
        <h2>{task.name}</h2>
        <div className="badge-row">
          <span className={`badge ${difficultyClass}`}>{task.difficulty}</span>
          <span className="badge badge-type">{task.type}</span>
          <span className="badge badge-type">{task.language}</span>
        </div>
      </div>

      <div className="detail-section">
        <h3>Task Statement</h3>
        <p className="statement-text">{task.statement}</p>
      </div>

      {task.difficultyNote && (
        <div className="detail-section">
          <h3>Difficulty Note</h3>
          <p className="statement-text">{task.difficultyNote}</p>
        </div>
      )}

      <div className="detail-section">
        <h3>Environment</h3>
        <div className="env-grid">
          <div className="env-item">
            <span className="env-label">Runtime</span>
            <span className="env-value">{task.environment?.runtime}</span>
          </div>
          <div className="env-item">
            <span className="env-label">Operating System</span>
            <span className="env-value">{task.environment?.os}</span>
          </div>
          <div className="env-item">
            <span className="env-label">Dependencies</span>
            <span className="env-value">{task.environment?.packages}</span>
          </div>
        </div>
        {task.environment?.details?.length > 0 && (
          <ul className="clean-list">
            {task.environment.details.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
      </div>

      {task.gradingCriteria?.length > 0 && (
        <div className="detail-section">
          <h3>Grading Criteria</h3>
          <ol className="clean-list">
            {task.gradingCriteria.map((criterion) => (
              <li key={criterion}>{criterion}</li>
            ))}
          </ol>
        </div>
      )}

      <div className="detail-section">
        <h3>Verification Commands</h3>
        <pre className="code-block">
          {`pytest ${task.graderPath} -v\ndocker build -t ${imageTag} -f ${task.environment?.dockerfile} .\ndocker run --rm ${imageTag}`}
        </pre>
      </div>
    </section>
  );
}
