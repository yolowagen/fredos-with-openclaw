# Nanobot Integration Guide

Version: v0.1
Status: canonical reference

---

## Overview

Nanobot is the **initial runtime/orchestration layer** for FredOS.
It does **not** own memory — FredOS does.

Nanobot should be treated as:
- Agent runner
- Tool host
- Message router
- Future multi-agent substrate

---

## Integration Boundary

FredOS exposes a REST API that Nanobot subagents call as tools.
No Nanobot agent should write directly to the FredOS database.

---

## Available FredOS API Endpoints

All endpoints are prefixed with `/api`.

### Projects
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/projects` | Create a project |
| GET | `/api/projects` | List projects (filter by `status`, `client_name`) |
| GET | `/api/projects/{id}` | Get a project |
| PATCH | `/api/projects/{id}` | Update a project |
| DELETE | `/api/projects/{id}` | Delete a project |

### Tasks
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks` | List tasks (filter by `project_id`, `status`) |
| GET | `/api/tasks/{id}` | Get a task |
| PATCH | `/api/tasks/{id}` | Update a task |
| DELETE | `/api/tasks/{id}` | Delete a task |

### Sessions
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/sessions` | Create a session |
| GET | `/api/sessions` | List sessions |
| GET | `/api/sessions/{id}` | Get a session |
| POST | `/api/sessions/{id}/summaries` | Add session summary |

### Research Notes
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/research-notes` | Create a research note |
| GET | `/api/research-notes` | List notes (filter by `project_id`, `task_id`) |

### Decisions
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/decisions` | Create a decision |
| GET | `/api/decisions` | List decisions (filter by `project_id`, `task_id`) |

### Memory
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/memory/items` | Create a memory item |
| GET | `/api/memory/items` | List items (filter by `project_id`, `memory_level`) |
| POST | `/api/memory/links` | Create a memory link |

### Retrieval (Policy-driven)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/retrieve/project-overview/{project_id}` | Mode A — "Where are we now?" |
| GET | `/api/retrieve/task-support/{task_id}` | Mode B — "Help me do this task" |
| GET | `/api/retrieve/research/{project_id}` | Mode C — "Investigate this issue" |
| GET | `/api/retrieve/personal-strategy` | Mode D — "How do I usually handle this?" |

### Consolidation
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/consolidate/{session_id}` | Consolidate session into project memory |

---

## Recommended Nanobot Agent Roles (v0.1)

### router-agent
- Classify incoming request
- Identify target project
- Choose retrieval mode
- Dispatch to correct subagent
- **Calls:** `GET /api/projects`, `GET /api/retrieve/project-overview/{id}`

### memory-curator-agent
- Summarise sessions
- Extract decisions and tasks
- Propose what to persist
- **Calls:** `POST /api/sessions/{id}/summaries`, `POST /api/consolidate/{id}`, `POST /api/memory/items`

### chief-of-staff-agent
- Generate daily briefs
- Identify blocked projects
- Recommend priorities
- **Calls:** `GET /api/projects`, `GET /api/tasks`, `GET /api/retrieve/project-overview/{id}`

### research-agent
- Investigate issues
- Create research notes
- **Calls:** `GET /api/retrieve/research/{id}`, `POST /api/research-notes`

---

## Example: Nanobot Tool Definition

```yaml
# nanobot tool config example
tools:
  - name: get_project_state
    description: Retrieve FredOS project state
    type: http
    config:
      method: GET
      url: "http://localhost:8000/api/projects/{project_id}"
    parameters:
      - name: project_id
        type: integer
        required: true

  - name: create_research_note
    description: Write a research note to FredOS
    type: http
    config:
      method: POST
      url: "http://localhost:8000/api/research-notes"
      body_schema:
        project_id: integer
        title: string
        question: string
        summary: string
```

---

## Key Rules

1. **Nanobot does not write directly to SQL** — always go through FredOS API.
2. **Memory ownership stays in FredOS** — if you switch runtimes, FredOS survives.
3. **Service-layer validation** — all writes are validated by FredOS services.
4. **Client isolation** — enforced at the FredOS layer, not the agent layer.
