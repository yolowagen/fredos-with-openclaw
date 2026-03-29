"""Decision service — CRUD for decisions."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.research import Decision


def create_decision(db: DBSession, **kwargs) -> Decision:
    decision = Decision(**kwargs)
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision


def get_decision(db: DBSession, decision_id: int) -> Optional[Decision]:
    return db.get(Decision, decision_id)


def list_decisions(
    db: DBSession,
    *,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
) -> list[Decision]:
    q = db.query(Decision)
    if project_id is not None:
        q = q.filter(Decision.project_id == project_id)
    if task_id is not None:
        q = q.filter(Decision.task_id == task_id)
    return q.order_by(Decision.created_at.desc()).all()


def delete_decision(db: DBSession, decision_id: int) -> bool:
    decision = db.get(Decision, decision_id)
    if decision is None:
        return False
    db.delete(decision)
    db.commit()
    return True
