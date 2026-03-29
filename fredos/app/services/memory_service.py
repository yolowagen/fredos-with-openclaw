"""Memory service — CRUD for memory items and memory links."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.memory import MemoryItem, MemoryLink


# ── Memory Items ──────────────────────────────────────────────

def create_memory_item(db: DBSession, **kwargs) -> MemoryItem:
    item = MemoryItem(**kwargs)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_memory_item(db: DBSession, item_id: int) -> Optional[MemoryItem]:
    return db.get(MemoryItem, item_id)


def list_memory_items(
    db: DBSession,
    *,
    project_id: Optional[int] = None,
    memory_level: Optional[str] = None,
    session_id: Optional[int] = None,
) -> list[MemoryItem]:
    q = db.query(MemoryItem)
    if project_id is not None:
        q = q.filter(MemoryItem.project_id == project_id)
    if memory_level:
        q = q.filter(MemoryItem.memory_level == memory_level)
    if session_id is not None:
        q = q.filter(MemoryItem.session_id == session_id)
    return q.order_by(MemoryItem.created_at.desc()).all()


def delete_memory_item(db: DBSession, item_id: int) -> bool:
    item = db.get(MemoryItem, item_id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True


# ── Memory Links ──────────────────────────────────────────────

def create_memory_link(db: DBSession, **kwargs) -> MemoryLink:
    link = MemoryLink(**kwargs)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def list_links_for(db: DBSession, memory_id: int) -> list[MemoryLink]:
    """Return all links FROM or TO the given memory item."""
    return (
        db.query(MemoryLink)
        .filter(
            (MemoryLink.from_memory_id == memory_id)
            | (MemoryLink.to_memory_id == memory_id)
        )
        .all()
    )
