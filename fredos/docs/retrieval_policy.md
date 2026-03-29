# FredOS Retrieval Policy

Version: v0.1
Status: canonical reference

---

## Principle

Retrieval is **not** "vector search over everything."
Each request gets a structured, priority-ordered memory slice.

---

## Default Retrieval Order

For any request, retrieve in this priority:

1. Relevant project canonical state
2. Open tasks for that project
3. Recent decisions
4. Recent session summaries
5. Related research notes
6. Supporting documents
7. Personal operating memory (if needed)

This keeps context compact and useful.

---

## Retrieval Modes

### Mode A — Project Overview

**Trigger:** "Where are we now?" / status check

**Returns:**
- Project summary & current state
- Next actions
- Blockers
- Recent decisions

---

### Mode B — Task Support

**Trigger:** "Help me do this task."

**Returns:**
- Task details & dependencies
- Related research notes
- Related documents
- Recent execution runs

---

### Mode C — Research

**Trigger:** "Investigate this issue."

**Returns:**
- Task context
- Project context
- Similar past research notes
- Supporting documents
- Open questions

---

### Mode D — Personal Strategy

**Trigger:** "How do I usually handle this?"

**Returns:**
- Personal operating memory (L3)
- Reusable methods
- Related prior decisions

---

## Implementation Notes

- Mode is determined by the Router Agent at dispatch time.
- `retrieval_service.py` implements each mode as a function.
- All queries filter by `project_id` first (unless Mode D).
- Results are capped and ordered by recency + importance score.
