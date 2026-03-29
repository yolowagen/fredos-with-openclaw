"""Retrieval service — policy-driven memory retrieval (modes A–D).

See docs/retrieval_policy.md for the design rationale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from sqlalchemy.orm import Session as DBSession

from app.models.project import Project, ProjectSnapshot
from app.models.task import Task
from app.models.research import Decision, ResearchNote
from app.models.session import SessionSummary
from app.models.document import Document
from app.models.memory import MemoryItem
from app.models.execution import ExecutionRun


@dataclass
class RetrievalResult:
    """Structured result returned by every retrieval mode."""

    mode: str
    project: Optional[dict] = None
    tasks: list[dict] = field(default_factory=list)
    decisions: list[dict] = field(default_factory=list)
    session_summaries: list[dict] = field(default_factory=list)
    research_notes: list[dict] = field(default_factory=list)
    documents: list[dict] = field(default_factory=list)
    execution_runs: list[dict] = field(default_factory=list)
    personal_memory: list[dict] = field(default_factory=list)


def _obj_to_dict(obj: Any) -> dict:
    """Cheaply serialise an ORM object for inclusion in RetrievalResult."""
    d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    # Convert datetimes to ISO strings for JSON friendliness.
    for k, v in d.items():
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()
    return d


# ── Mode A — Project Overview ────────────────────────────────

def retrieve_project_overview(
    db: DBSession, project_id: int, *, limit: int = 10
) -> RetrievalResult:
    """'Where are we now?' — project summary, actions, blockers, decisions."""
    result = RetrievalResult(mode="A")

    project = db.get(Project, project_id)
    if project is None:
        return result
    result.project = _obj_to_dict(project)

    result.decisions = [
        _obj_to_dict(d)
        for d in db.query(Decision)
        .filter(Decision.project_id == project_id)
        .order_by(Decision.created_at.desc())
        .limit(limit)
        .all()
    ]

    result.session_summaries = [
        _obj_to_dict(s)
        for s in db.query(SessionSummary)
        .join(SessionSummary.session)
        .filter(SessionSummary.session.has(project_id=project_id))
        .order_by(SessionSummary.created_at.desc())
        .limit(limit)
        .all()
    ]

    return result


# ── Mode B — Task Support ────────────────────────────────────

def retrieve_task_support(
    db: DBSession, task_id: int, *, limit: int = 10
) -> RetrievalResult:
    """'Help me do this task.' — task + deps + research + docs + runs."""
    result = RetrievalResult(mode="B")

    task = db.get(Task, task_id)
    if task is None:
        return result
    result.tasks = [_obj_to_dict(task)]

    result.research_notes = [
        _obj_to_dict(n)
        for n in db.query(ResearchNote)
        .filter(ResearchNote.task_id == task_id)
        .order_by(ResearchNote.created_at.desc())
        .limit(limit)
        .all()
    ]

    result.documents = [
        _obj_to_dict(d)
        for d in db.query(Document)
        .filter(Document.project_id == task.project_id)
        .order_by(Document.updated_at.desc())
        .limit(limit)
        .all()
    ]

    result.execution_runs = [
        _obj_to_dict(r)
        for r in db.query(ExecutionRun)
        .filter(ExecutionRun.task_id == task_id)
        .order_by(ExecutionRun.created_at.desc())
        .limit(limit)
        .all()
    ]

    return result


# ── Mode C — Research ─────────────────────────────────────────

def retrieve_research(
    db: DBSession, project_id: int, *, limit: int = 10
) -> RetrievalResult:
    """'Investigate this issue.' — context + past research + open questions."""
    result = RetrievalResult(mode="C")

    project = db.get(Project, project_id)
    if project:
        result.project = _obj_to_dict(project)

    result.research_notes = [
        _obj_to_dict(n)
        for n in db.query(ResearchNote)
        .filter(ResearchNote.project_id == project_id)
        .order_by(ResearchNote.created_at.desc())
        .limit(limit)
        .all()
    ]

    result.documents = [
        _obj_to_dict(d)
        for d in db.query(Document)
        .filter(Document.project_id == project_id)
        .order_by(Document.updated_at.desc())
        .limit(limit)
        .all()
    ]

    result.tasks = [
        _obj_to_dict(t)
        for t in db.query(Task)
        .filter(Task.project_id == project_id, Task.status == "open")
        .order_by(Task.updated_at.desc())
        .limit(limit)
        .all()
    ]

    return result


# ── Mode D — Personal Strategy ────────────────────────────────

def retrieve_personal_strategy(
    db: DBSession, *, limit: int = 20
) -> RetrievalResult:
    """'How do I usually handle this?' — L3 memory + reusable methods."""
    result = RetrievalResult(mode="D")

    result.personal_memory = [
        _obj_to_dict(m)
        for m in db.query(MemoryItem)
        .filter(MemoryItem.memory_level == "L3")
        .order_by(MemoryItem.importance_score.desc().nulls_last())
        .limit(limit)
        .all()
    ]

    result.decisions = [
        _obj_to_dict(d)
        for d in db.query(Decision)
        .order_by(Decision.created_at.desc())
        .limit(limit)
        .all()
    ]

    return result
