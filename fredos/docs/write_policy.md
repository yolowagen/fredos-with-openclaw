# FredOS Write Policy

Version: v0.1
Status: canonical reference

---

## Principle

No raw LLM output should become canonical memory without consolidation.
All writes follow a three-step pipeline.

---

## Step 1 — Capture

Store raw input as one of:

| Source Type | Destination |
|-------------|-------------|
| External message | `inbox_items` |
| Work during session | `sessions` (events) |
| Quick note | `memory_items` (L0/L1) |
| Tool output | `execution_runs` |

At this stage, data is unprocessed and unlinked.

---

## Step 2 — Consolidate

The Memory Curator Agent (or `consolidation_service`) decides whether to create:

- **Project snapshot** — periodic summary of project state
- **Research note** — distilled investigation output
- **Decision** — explicit choice made with context
- **Session summary** — what happened, open loops, extracted items
- **Reusable pattern** — method worth remembering (L3)

Each created item gets an `importance_score` and `sensitivity` classification.

---

## Step 3 — Link

Create explicit links between related entities:

| From | To | Relation Type |
|------|----|---------------|
| Session | Project | `belongs_to` |
| Task | Research Note | `informed_by` |
| Decision | Task | `decided_for` |
| Document | Project | `supports` |
| Memory Item | Source Item | `derived_from` |

Links are stored in `memory_links` with typed relations.

---

## Rules

1. **Service-layer validation** — all writes go through service modules, never direct DB inserts.
2. **Client isolation** — a write must be associated with a project; cross-client writes are rejected.
3. **Idempotency** — re-consolidating a session should not create duplicate entries.
4. **Audit trail** — every write records `created_by` (agent name or `user`).
