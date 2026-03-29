"""Chief of Staff Agent — global overview and prioritisation.

Model: medium / large
Purpose: generate daily briefs, identify blocked projects, recommend top priorities,
         send stale-project reminders.

Outputs:
- Daily brief
- Blocked project report
- Top priorities
- Stale project reminders

Status: STUB — awaiting Nanobot integration and retrieval stability.
"""

from __future__ import annotations


def generate_daily_brief() -> dict:
    """Compile a daily brief across all active projects.

    TODO: Implement with LLM call — reads all active projects via
    retrieval_service.retrieve_project_overview() for each project.
    """
    return {"status": "stub", "brief": None}


def identify_blocked_projects() -> list[dict]:
    """Return a list of projects that appear blocked.

    TODO: Implement by analysing project states and task statuses.
    """
    return []


def recommend_priorities() -> list[str]:
    """Suggest the top priorities for today.

    TODO: Implement with LLM reasoning over project states.
    """
    return []
