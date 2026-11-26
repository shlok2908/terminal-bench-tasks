import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import cors from "cors";
import express from "express";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const TASKS_ROOT = path.resolve(__dirname, "..", "tasks");

const TASK_CATALOG = [
  {
    id: "TASK-001",
    slug: "task-001-number-statistics",
    name: "Fix Number Statistics Program",
    type: "Language-driven",
    language: "Python",
    difficulty: "Easy",
    sourceFile: "tasks/task-001-number-statistics/src/statistics.py",
    graderPath: "tasks/task-001-number-statistics/grader/",
    dockerfile: "tasks/task-001-number-statistics/environment/Dockerfile",
  },
  {
    id: "TASK-002",
    slug: "task-002-task-tracker",
    name: "Improve Task Tracking Results",
    type: "Outcome-driven",
    language: "Python",
    difficulty: "Medium",
    sourceFile: "tasks/task-002-task-tracker/src/task_tracker.py",
    graderPath: "tasks/task-002-task-tracker/grader/",
    dockerfile: "tasks/task-002-task-tracker/environment/Dockerfile",
  },
];

function extractSection(markdown, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`## ${escaped}\\r?\\n([\\s\\S]*?)(?=\\r?\\n## |$)`);
  const match = markdown.match(pattern);
  return match ? match[1].trim() : "";
}

function extractBullets(sectionText) {
  return sectionText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "))
    .map((line) => line.slice(2).trim());
}

function extractNumberedList(sectionText) {
  return sectionText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => /^\d+\.\s+/.test(line))
    .map((line) => line.replace(/^\d+\.\s+/, "").trim());
}

function loadTasks() {
  return TASK_CATALOG.map((meta) => {
    const statementPath = path.join(TASKS_ROOT, meta.slug, "statement.md");
    const rawMarkdown = fs.existsSync(statementPath)
      ? fs.readFileSync(statementPath, "utf8")
      : "";

    const statement = extractSection(rawMarkdown, "Statement");
    const environmentItems = extractBullets(extractSection(rawMarkdown, "Environment"));
    const difficultyNote = extractSection(rawMarkdown, "Difficulty Note");
    const gradingCriteria = extractNumberedList(
      extractSection(rawMarkdown, "Grading Criteria")
    );

    return {
      id: meta.id,
      slug: meta.slug,
      name: meta.name,
      type: meta.type,
      language: meta.language,
      difficulty: meta.difficulty,
      statement,
      fullStatementMarkdown: rawMarkdown,
      difficultyNote,
      environment: {
        runtime: "Python 3.11+",
        os: "Linux-based environment",
        packages: "No external Python packages required",
        dockerfile: meta.dockerfile,
        details: environmentItems,
      },
      gradingCriteria,
      sourceFile: meta.sourceFile,
      graderPath: meta.graderPath,
    };
  });
}

const app = express();
const PORT = Number(process.env.PORT) || 3001;

app.use(cors());
app.use(express.json());

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.get("/api/tasks", (_req, res) => {
  try {
    const tasks = loadTasks();
    res.json({ tasks });
  } catch (error) {
    res.status(500).json({ error: "Failed to load benchmark tasks", details: error.message });
  }
});

app.get("/api/tasks/:id", (req, res) => {
  try {
    const tasks = loadTasks();
    const target = tasks.find(
      (task) =>
        task.id.toLowerCase() === req.params.id.toLowerCase() ||
        task.slug.toLowerCase() === req.params.id.toLowerCase()
    );
    if (!target) {
      return res.status(404).json({ error: "Task not found" });
    }
    return res.json({ task: target });
  } catch (error) {
    return res
      .status(500)
      .json({ error: "Failed to load benchmark task", details: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Terminal-Bench backend listening on http://localhost:${PORT}`);
});
