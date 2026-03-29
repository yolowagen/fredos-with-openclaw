"""Bridge API routes — OpenClaw ↔ FredOS session bridge.

These endpoints are called by the FredOS OpenClaw plugin via hooks:
  agent_end        → POST /api/bridge/ingest-turn
  after_compaction → POST /api/bridge/ingest-summary
  before_reset     → POST /api/bridge/finalize-session
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from app.db import get_db
from app.schemas.bridge import (
    IngestTurnRequest,
    IngestTurnResponse,
    IngestSummaryRequest,
    IngestSummaryResponse,
    FinalizeSessionRequest,
    FinalizeSessionResponse,
)
from app.services import bridge_service

bridge_router = APIRouter(prefix="/bridge", tags=["Bridge"])


@bridge_router.post("/ingest-turn", response_model=IngestTurnResponse)
def ingest_turn(body: IngestTurnRequest, db: DBSession = Depends(get_db)):
    """Ingest a single OpenClaw conversation turn into FredOS L0 memory."""
    result = bridge_service.ingest_turn(
        db,
        openclaw_session_id=body.openclaw_session_id,
        openclaw_session_key=body.openclaw_session_key,
        openclaw_agent_id=body.openclaw_agent_id,
        project_id=body.project_id,
        user_message=body.user_message,
        assistant_message=body.assistant_message,
        tool_calls=body.tool_calls,
        duration_ms=body.duration_ms,
        success=body.success,
    )
    return result


@bridge_router.post("/ingest-summary", response_model=IngestSummaryResponse)
def ingest_summary(body: IngestSummaryRequest, db: DBSession = Depends(get_db)):
    """Store a compaction summary from OpenClaw into FredOS as SessionSummary."""
    result = bridge_service.ingest_summary(
        db,
        openclaw_session_id=body.openclaw_session_id,
        openclaw_session_key=body.openclaw_session_key,
        openclaw_agent_id=body.openclaw_agent_id,
        project_id=body.project_id,
        summary_text=body.summary_text,
        message_count=body.message_count,
        compacted_count=body.compacted_count,
    )
    return result


@bridge_router.post("/finalize-session", response_model=FinalizeSessionResponse)
def finalize_session(body: FinalizeSessionRequest, db: DBSession = Depends(get_db)):
    """Finalize an OpenClaw session, triggering FredOS consolidation (L0 → L2)."""
    result = bridge_service.finalize_session(
        db,
        openclaw_session_id=body.openclaw_session_id,
        openclaw_session_key=body.openclaw_session_key,
        openclaw_agent_id=body.openclaw_agent_id,
        project_id=body.project_id,
        reason=body.reason,
    )
    return result
