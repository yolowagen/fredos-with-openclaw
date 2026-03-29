"""Router Agent — triage and dispatch incoming requests.

Model: small / cheap / fast
Purpose: classify intent, identify project, choose workflow, dispatch to subagent.

Inputs:
- Incoming message
- Active project summaries (via retrieval_service Mode A)
- Open sessions
- Recent inbox items

Outputs:
- Target project
- Action type (task, research, status-check, etc.)
- Whether task creation is needed
- Whether research is needed
- Subagent route

Status: STUB — awaiting Nanobot integration and retrieval stability.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.models.task import Task


@dataclass
class RoutingDecision:
    """Result of the router's analysis."""

    target_project_id: Optional[int] = None
    action_type: str = "unknown"  # task | research | status | dispatch
    needs_task_creation: bool = False
    needs_research: bool = False
    subagent_route: Optional[str] = None  # memory-curator | research | chief-of-staff
    confidence: float = 0.0


def route_request(message: str) -> RoutingDecision:
    """Classify an incoming message and decide where it should go.

    TODO: Implement with LLM call via Nanobot runtime.
    """
    return RoutingDecision(action_type="unknown")


def route_task(task: Task) -> str:
    """Deterministic routing logic based on task attributes (Phase 7)."""
    if task.task_type == "research":
        return "research_agent"
    elif task.task_type == "memory_update":
        return "memory_curator_agent"
    elif task.task_type == "planning":
        return "chief_of_staff_agent"
    else:
        return "router_agent"
