"""Memory Curator Agent — convert raw work into useful long-term memory.

Model: medium
Purpose: summarise sessions, extract decisions, recommend what to persist,
         generate project snapshots, identify reusable patterns.

Inputs:
- Session transcript summary
- Task updates
- Research outputs
- Decisions made

Outputs:
- Session summary
- Decision extraction
- Project snapshot proposal
- Memory item importance score

Status: STUB — awaiting Nanobot integration.
"""

from __future__ import annotations

from typing import Optional


def curate_session(session_id: int) -> dict:
    """Analyse a session and propose memory items to persist.

    TODO: Implement with LLM call via Nanobot runtime.
    Currently, use consolidation_service.consolidate_session() for
    the deterministic version of this workflow.
    """
    return {"status": "stub", "session_id": session_id}


def propose_snapshot(project_id: int) -> Optional[dict]:
    """Generate a project snapshot proposal for review.

    TODO: Implement with LLM summarisation.
    """
    return None


def score_importance(content: str) -> float:
    """Estimate the importance score (0.0–1.0) of a memory item.

    TODO: Implement with LLM or heuristic.
    """
    return 0.5
