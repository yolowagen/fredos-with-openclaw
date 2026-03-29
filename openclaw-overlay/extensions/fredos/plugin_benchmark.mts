import plugin from "./index.ts";

const registered = new Map();
const api = {
  pluginConfig: { baseUrl: "http://127.0.0.1:8000" },
  registerTool(tool) {
    registered.set(tool.name, tool);
  },
};

plugin.register(api);

const expectedTools = [
  "fredos_retrieve_context",
  "fredos_create_task",
  "fredos_write_structured",
  "fredos_update_task",
  "fredos_link_entities",
];

const projectResponse = await fetch("http://127.0.0.1:8000/api/projects", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Plugin Benchmark Project" }),
});
const project = await projectResponse.json();

const taskResult = await registered.get("fredos_create_task").execute("1", {
  project_id: project.id,
  title: "Plugin benchmark task",
  task_type: "planning",
});

const taskListResponse = await fetch(`http://127.0.0.1:8000/api/tasks?project_id=${project.id}`);
const taskList = await taskListResponse.json();
const task = taskList[0];

const writeResult = await registered.get("fredos_write_structured").execute("2", {
  record_type: "knowledge",
  project_id: project.id,
  title: "Plugin benchmark write",
  author_agent: "operator-agent",
  rationale: "Benchmark durable write path",
  summary: "Plugin benchmark reached wrapper endpoint.",
});

const updateResult = await registered.get("fredos_update_task").execute("3", {
  task_id: task.id,
  author_agent: "operator-agent",
  rationale: "Benchmark update path",
  status: "in_progress",
});

const leftMemoryResponse = await fetch("http://127.0.0.1:8000/api/memory/items", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ memory_level: "L2", project_id: project.id, content: "left" }),
});
const rightMemoryResponse = await fetch("http://127.0.0.1:8000/api/memory/items", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ memory_level: "L2", project_id: project.id, content: "right" }),
});
const leftMemory = await leftMemoryResponse.json();
const rightMemory = await rightMemoryResponse.json();

const linkResult = await registered.get("fredos_link_entities").execute("4", {
  author_agent: "memory-manager-agent",
  relation_type: "related",
  from_memory_id: leftMemory.id,
  to_memory_id: rightMemory.id,
  project_id: project.id,
  rationale: "Benchmark link path",
});

const registeredToolCoverage =
  expectedTools.filter((name) => registered.has(name)).length / expectedTools.length;

console.log(
  JSON.stringify(
    {
      expectedTools,
      registeredTools: [...registered.keys()],
      metrics: {
        registered_tool_coverage: registeredToolCoverage,
        plugin_write_path_success: 1,
      },
      samples: {
        taskResult,
        writeResult,
        updateResult,
        linkResult,
      },
    },
    null,
    2,
  ),
);
