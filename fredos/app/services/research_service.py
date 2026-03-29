"""Research service — CRUD for research notes."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.research import ResearchNote


def create_research_note(db: DBSession, **kwargs) -> ResearchNote:
    note = ResearchNote(**kwargs)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_research_note(db: DBSession, note_id: int) -> Optional[ResearchNote]:
    return db.get(ResearchNote, note_id)


def list_research_notes(
    db: DBSession,
    *,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
) -> list[ResearchNote]:
    q = db.query(ResearchNote)
    if project_id is not None:
        q = q.filter(ResearchNote.project_id == project_id)
    if task_id is not None:
        q = q.filter(ResearchNote.task_id == task_id)
    return q.order_by(ResearchNote.created_at.desc()).all()


def delete_research_note(db: DBSession, note_id: int) -> bool:
    note = db.get(ResearchNote, note_id)
    if note is None:
        return False
    db.delete(note)
    db.commit()
    return True
