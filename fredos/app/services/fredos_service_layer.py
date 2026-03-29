"""Structured service layer wrappers for governed FredOS access."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session as DBSession

from app.services import decision_service, memory_service, research_service, task_service


def _require_author(author_agent: str) -> None:
    if not author_agent or not author_agent.strip():
        raise HTTPException(status_code=400, detail="author_agent is required")


def _require_rationale(rationale: str | None) -> None:
    if not rationale or not rationale.strip():
        raise HTTPException(status_code=400, detail="rationale is required for durable writes")


def write_structured(
    db: DBSession,
    *,
    record_type: str,
    project_id: int,
    title: str,
    author_agent: str,
    rationale: str | None = None,
    task_id: int | None = None,
    summary: str | None = None,
    content: str | None = None,
    recommendations: str | None = None,
    confidence: float | None = None,
    source_refs: str | None = None,
) -> dict:
    _require_author(author_agent)
    _require_rationale(rationale)

    if record_type == "task":
        task = task_service.create_task(
            db,
            project_id=project_id,
            title=title,
            description=content or summary or rationale,
            task_type="structured_write",
            owner_type="agent",
            owner_name=author_agent,
            needs_research=False,
            needs_execution=False,
        )
        return {
            "record_type": "task",
            "record_id": task.id,
            "project_id": project_id,
            "status": "created",
        }

    if record_type == "decision":
        decision = decision_service.create_decision(
            db,
            project_id=project_id,
            task_id=task_id,
            title=title,
            context=rationale,
            decision_made=summary or content,
            reasoning_summary=recommendations,
            tradeoffs=f"confidence={confidence}" if confidence is not None else None,
            decided_by=author_agent,
        )
        return {
            "record_type": "decision",
            "record_id": decision.id,
            "project_id": project_id,
            "status": "created",
        }

    if record_type == "knowledge":
        note = research_service.create_research_note(
            db,
            project_id=project_id,
            task_id=task_id,
            title=title,
            question=rationale,
            summary=summary or content,
            recommendations=recommendations,
            source_refs=source_refs,
            created_by=author_agent,
        )
        return {
            "record_type": "knowledge",
            "record_id": note.id,
            "project_id": project_id,
            "status": "created",
        }

    raise HTTPException(status_code=400, detail=f"Unsupported record_type: {record_type}")


def update_task_structured(
    db: DBSession,
    task_id: int,
    *,
    author_agent: str,
    rationale: str | None = None,
    **updates,
) -> dict:
    _require_author(author_agent)
    _require_rationale(rationale)

    allowed_updates = {key: value for key, value in updates.items() if value is not None}
    if not allowed_updates:
        raise HTTPException(status_code=400, detail="No task fields supplied for update")

    task = task_service.update_task(db, task_id, **allowed_updates)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "record_type": "task",
        "record_id": task.id,
        "project_id": task.project_id,
        "status": "updated",
    }


def link_entities(
    db: DBSession,
    *,
    author_agent: str,
    relation_type: str,
    from_memory_id: int | None = None,
    to_memory_id: int | None = None,
    project_id: int | None = None,
    task_id: int | None = None,
    rationale: str | None = None,
) -> dict:
    _require_author(author_agent)
    _require_rationale(rationale)

    if from_memory_id and to_memory_id:
        link = memory_service.create_memory_link(
            db,
            from_memory_id=from_memory_id,
            to_memory_id=to_memory_id,
            relation_type=relation_type,
        )
        return {
            "record_type": "memory_link",
            "record_id": link.id,
            "project_id": project_id or 0,
            "status": "created",
        }

    if project_id and task_id:
        memory = memory_service.create_memory_item(
            db,
            memory_level="L2",
            project_id=project_id,
            task_id=task_id,
            source_type="task_link",
            summary=rationale,
            content=f"Linked task {task_id} to project {project_id} as {relation_type}",
        )
        return {
            "record_type": "memory_item",
            "record_id": memory.id,
            "project_id": project_id,
            "status": "created",
        }

    raise HTTPException(
        status_code=400,
        detail="Provide either from_memory_id/to_memory_id or project_id/task_id",
    )
