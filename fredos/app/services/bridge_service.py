"""Bridge service — maps OpenClaw sessions into FredOS memory.

Handles three operations:
1. ingest_turn  — store a conversation turn as L0 memory
2. ingest_summary — store a compaction summary as SessionSummary
3. finalize_session — trigger consolidation (L0 → L2)
"""

from __future__ import annotations

import json
import datetime as dt
from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.memory import MemoryItem
from app.models.session import Session, SessionSummary
from app.services import consolidation_service


# ── Agent → Project mapping ──────────────────────────────────
# Option E: known agents map to default projects; unknown agents
# go to a catch-all project.  The catch-all is created on first use.

CATCH_ALL_PROJECT_NAME = "OpenClaw Conversations"


def _resolve_project_id(
    db: DBSession,
    agent_id: str,
    explicit_project_id: Optional[int],
) -> int:
    """Determine which FredOS project to associate with this session."""
    if explicit_project_id is not None:
        return explicit_project_id

    # Fallback: find or create the catch-all project
    from app.models.project import Project

    catch_all = (
        db.query(Project)
        .filter(Project.name == CATCH_ALL_PROJECT_NAME)
        .first()
    )
    if catch_all:
        return catch_all.id

    catch_all = Project(
        name=CATCH_ALL_PROJECT_NAME,
        status="active",
        objective="Captures all OpenClaw conversations that are not linked to a specific project.",
    )
    db.add(catch_all)
    db.flush()
    return catch_all.id


def _resolve_session(
    db: DBSession,
    openclaw_session_id: str,
    openclaw_session_key: str,
    openclaw_agent_id: str,
    project_id: int,
) -> Session:
    """Find or create a FredOS Session for the given OpenClaw session instance."""
    existing = (
        db.query(Session)
        .filter(Session.openclaw_session_id == openclaw_session_id)
        .first()
    )
    if existing:
        return existing

    new_session = Session(
        project_id=project_id,
        title=f"OpenClaw [{openclaw_agent_id}] session",
        status="active",
        goal=f"Auto-created from OpenClaw agent '{openclaw_agent_id}'",
        openclaw_session_id=openclaw_session_id,
        openclaw_session_key=openclaw_session_key,
        openclaw_agent_id=openclaw_agent_id,
        started_at=dt.datetime.utcnow(),
    )
    db.add(new_session)
    db.flush()
    return new_session


# ── Public API ────────────────────────────────────────────────


def ingest_turn(
    db: DBSession,
    *,
    openclaw_session_id: str,
    openclaw_session_key: str,
    openclaw_agent_id: str,
    project_id: Optional[int],
    user_message: str,
    assistant_message: str,
    tool_calls: Optional[list[dict]],
    duration_ms: Optional[int],
    success: bool,
) -> dict:
    """Store a single conversation turn as L0 working memory."""
    pid = _resolve_project_id(db, openclaw_agent_id, project_id)
    session = _resolve_session(
        db,
        openclaw_session_id,
        openclaw_session_key,
        openclaw_agent_id,
        pid,
    )

    # Build content blob
    content_parts = [
        f"[User] {user_message}",
        f"[Assistant] {assistant_message}",
    ]
    if tool_calls:
        tool_names = [tc.get("name", "unknown") for tc in tool_calls]
        content_parts.append(f"[Tools used] {', '.join(tool_names)}")

    content = "\n\n".join(content_parts)

    mi = MemoryItem(
        memory_level="L0",
        project_id=session.project_id,
        session_id=session.id,
        source_type="openclaw_turn",
        content=content,
        summary=assistant_message[:200] if assistant_message else None,
        importance_score=0.3,
    )
    db.add(mi)
    db.commit()
    db.refresh(mi)

    return {
        "fredos_session_id": session.id,
        "memory_item_id": mi.id,
        "status": "ingested",
    }


def ingest_summary(
    db: DBSession,
    *,
    openclaw_session_id: str,
    openclaw_session_key: str,
    openclaw_agent_id: str,
    project_id: Optional[int],
    summary_text: str,
    message_count: int,
    compacted_count: int,
) -> dict:
    """Store a compaction summary as a FredOS SessionSummary."""
    pid = _resolve_project_id(db, openclaw_agent_id, project_id)
    session = _resolve_session(
        db,
        openclaw_session_id,
        openclaw_session_key,
        openclaw_agent_id,
        pid,
    )

    ss = SessionSummary(
        session_id=session.id,
        summary=summary_text,
        open_loops=f"Compacted {compacted_count}/{message_count} messages",
    )
    db.add(ss)
    db.commit()
    db.refresh(ss)

    return {
        "fredos_session_id": session.id,
        "summary_id": ss.id,
        "status": "summary_stored",
    }


def finalize_session(
    db: DBSession,
    *,
    openclaw_session_id: str,
    openclaw_session_key: str,
    openclaw_agent_id: str,
    project_id: Optional[int],
    reason: str,
) -> dict:
    """Finalize a FredOS session and trigger consolidation."""
    session = (
        db.query(Session)
        .filter(Session.openclaw_session_id == openclaw_session_id)
        .first()
    )
    if session is None and project_id is not None:
        session = _resolve_session(
            db,
            openclaw_session_id,
            openclaw_session_key,
            openclaw_agent_id,
            _resolve_project_id(db, openclaw_agent_id, project_id),
        )
    if session is None:
        return {
            "fredos_session_id": 0,
            "consolidation_result": {"info": "No FredOS session found for this key"},
            "status": "no_session",
        }

    # Mark session as ended
    session.ended_at = dt.datetime.utcnow()
    db.flush()

    # Run consolidation
    result = consolidation_service.consolidate_session(db, session.id)

    return {
        "fredos_session_id": session.id,
        "consolidation_result": result,
        "status": "finalized",
    }
