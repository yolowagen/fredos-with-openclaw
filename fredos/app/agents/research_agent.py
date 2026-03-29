"""Research Agent — issue investigation and knowledge generation.

Model: medium / large
Purpose: investigate issues, generate hypotheses, create research notes,
         recommend actions, provide supporting references.

Outputs:
- Research note
- Hypotheses
- Recommended actions
- Supporting references

Status: STUB — awaiting Nanobot integration.
"""

from __future__ import annotations

from typing import Optional


def investigate(project_id: int, question: str) -> dict:
    """Investigate a question in the context of a project.

    TODO: Implement with LLM call via Nanobot runtime.
    Should use retrieval_service.retrieve_research() to gather context.
    """
    return {
        "status": "stub",
        "project_id": project_id,
        "question": question,
        "hypotheses": [],
        "recommendations": [],
    }


def generate_research_note(
    project_id: int,
    task_id: Optional[int],
    question: str,
) -> Optional[dict]:
    """Create a structured research note from investigation results.

    TODO: Implement with LLM — calls investigate() then writes via
    research_service.create_research_note().
    """
    return None
