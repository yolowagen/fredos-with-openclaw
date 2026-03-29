"""Task Queue service — Phase 8."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.task import Task
from app.services import event_service

def pick_next_task(db: DBSession, actor: str = "system") -> Optional[Task]:
    """Retrieve the oldest unassigned 'open' task and lock it as 'in_progress'.
    
    This acts as a primitive SQLite-backed queue worker pull.
    """
    # Simply pick the oldest Open task
    task = (
        db.query(Task)
        .filter(Task.status == "open")
        .order_by(Task.created_at.asc())
        .first()
    )
    
    if not task:
        return None

    # Locking mechanism
    task.status = "in_progress"
    task.started_at = dt.datetime.now(dt.timezone.utc)
    
    db.commit()
    db.refresh(task)
    
    event_service.emit_event(
        db, 
        event_type="queue_task_picked", 
        actor=actor, 
        payload={"task_id": task.id, "task_type": task.task_type}
    )
    
    return task
