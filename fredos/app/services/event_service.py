"""Event service — Phase 7."""

from __future__ import annotations

import json
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.event_log import EventLog


def emit_event(
    db: DBSession, event_type: str, actor: str, payload: Optional[dict] = None
) -> EventLog:
    """Commit a global event to the timeline."""
    event = EventLog(
        event_type=event_type,
        actor=actor,
        payload=json.dumps(payload) if payload else None,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events(db: DBSession, limit: int = 50) -> list[EventLog]:
    """Retrieve recent events."""
    return db.query(EventLog).order_by(EventLog.created_at.desc()).limit(limit).all()
