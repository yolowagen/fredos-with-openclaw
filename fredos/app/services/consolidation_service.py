"""Consolidation service — harvest session outputs into project memory.

Implements the first meaningful memory workflow:
``consolidate_session(session_id)``

See docs/write_policy.md for the three-step pipeline (capture → consolidate → link).
"""

from __future__ import annotations

import json
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.session import Session, SessionSummary
from app.models.memory import MemoryItem, MemoryLink
from app.models.project import ProjectSnapshot


def consolidate_session(db: DBSession, session_id: int) -> dict:
    """Consolidate a session into project memory.

    Steps performed:
    1. Load the session and its summaries.
    2. If no summary exists, create a placeholder summary.
    3. Promote extracted items into memory_items at L2.
    4. Create a project snapshot recording the consolidation.
    5. Mark the session as 'consolidated'.

    Returns a dict summarising what was created.
    """
    session = db.get(Session, session_id)
    if session is None:
        return {"error": f"Session {session_id} not found"}

    if session.status == "consolidated":
        return {"info": "Session already consolidated", "session_id": session_id}

    created: dict = {"memory_items": [], "snapshot": None}

    # ── Step 1: gather summaries ──────────────────────────────
    summaries = (
        db.query(SessionSummary)
        .filter(SessionSummary.session_id == session_id)
        .all()
    )

    if not summaries:
        # Auto-create a minimal placeholder summary.
        placeholder = SessionSummary(
            session_id=session_id,
            summary=f"Auto-consolidated session: {session.title or session_id}",
        )
        db.add(placeholder)
        db.flush()
        summaries = [placeholder]

    # ── Step 2: promote to memory items (L2) ──────────────────
    for s in summaries:
        mi = MemoryItem(
            memory_level="L2",
            project_id=session.project_id,
            session_id=session_id,
            source_type="session_summary",
            content=s.summary,
            summary=s.summary[:200] if s.summary else None,
            importance_score=0.6,
        )
        db.add(mi)
        db.flush()
        created["memory_items"].append(mi.id)

        # Try to extract tasks / decisions from JSON fields
        _promote_extracted(db, s, mi, session)

    # ── Step 3: create project snapshot ───────────────────────
    combined_summary = " | ".join(
        s.summary or "" for s in summaries
    )
    snapshot = ProjectSnapshot(
        project_id=session.project_id,
        summary=f"Consolidated from session {session_id}: {combined_summary[:300]}",
        created_by="consolidation_service",
    )
    db.add(snapshot)
    db.flush()
    created["snapshot"] = snapshot.id

    # ── Step 4: mark session as consolidated ──────────────────
    session.status = "consolidated"
    db.commit()

    return {
        "session_id": session_id,
        "status": "consolidated",
        "created": created,
    }


def _promote_extracted(
    db: DBSession,
    summary: SessionSummary,
    parent_mi: MemoryItem,
    session: Session,
) -> None:
    """If extracted_tasks or extracted_decisions exist (JSON), create child memory items."""
    for field_name in ("extracted_tasks", "extracted_decisions"):
        raw = getattr(summary, field_name, None)
        if not raw:
            continue
        try:
            items = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        if not isinstance(items, list):
            continue
        for item_text in items:
            child = MemoryItem(
                memory_level="L2",
                project_id=session.project_id,
                session_id=session.id,
                source_type=field_name,
                content=str(item_text),
                summary=str(item_text)[:200],
                importance_score=0.5,
            )
            db.add(child)
            db.flush()
            # Link child → parent
            link = MemoryLink(
                from_memory_id=child.id,
                to_memory_id=parent_mi.id,
                relation_type="derived_from",
            )
            db.add(link)
