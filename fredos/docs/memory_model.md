# FredOS Memory Model

Version: v0.1
Status: canonical reference

---

## Overview

FredOS memory is layered into five levels (L0–L4) plus a governance layer.
State lives in SQL. Artifacts live in the filesystem. References between them live in SQL.

---

## L0 — Working Memory

Short-lived context during a single action.

| Content | Persistence |
|---------|-------------|
| Current prompt context | Ephemeral |
| Temporary tool output | Ephemeral |
| Scratch reasoning summaries | Ephemeral |

Only elevated outputs are saved — most L0 data is discarded after use.

---

## L1 — Session Memory

A bounded work episode (e.g. one investigation, one coding cycle).

**Stores:**
- Session goal
- Materials read
- Hypotheses
- Unfinished loops
- Extracted candidate tasks
- Extracted decisions

**Lifecycle:** Created at session start → populated during work → consolidated into L2 at session end.

---

## L2 — Project Memory

Canonical project-level state. One record per project.

**Stores:**
- Objective & current state
- Phase & status
- Active tasks & blockers
- Key decisions
- Recent snapshots
- Project vocabulary / domain context

**Sources:** Consolidated from L1 sessions, direct writes via service APIs.

---

## L3 — Personal Operating Memory

Long-term memory about how Fred works — not project-specific.

**Stores:**
- Work principles
- Decision style
- Reusable methods
- Delivery preferences
- Capability map
- Client separation rules

---

## L4 — Knowledge / Artifact Memory

Document and evidence layer.

**Stores:**
- Specs, reports, issue briefs
- Meeting notes
- Test results
- Linked files
- Repo summaries

**Storage:** Artifact files on filesystem, metadata + references in SQL.

---

## Governance Layer

Controls what gets persisted, summarized, or stays ephemeral.

| Concern | Mechanism |
|---------|-----------|
| Persistence gate | Memory Curator decides what to elevate |
| Summarization | Session → summary; snapshot generation |
| Sensitivity classification | Per-item `sensitivity` field |
| Client isolation | `client_name` on projects, no cross-client retrieval |
| Archival / retention | Future: retention policies per memory level |

---

## Entity–Layer Mapping

| SQL Table | Primary Layer |
|-----------|---------------|
| `sessions`, `session_summaries` | L1 |
| `projects`, `project_snapshots` | L2 |
| `tasks`, `task_dependencies` | L2 |
| `decisions` | L2 |
| `research_notes` | L2 / L4 |
| `memory_items`, `memory_links` | Any (field: `memory_level`) |
| `documents` | L4 |
| `inbox_items` | L0 → L1 intake |
| `execution_runs` | L1 |
| `daily_briefs` | L2 / L3 |
