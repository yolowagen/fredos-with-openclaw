"""Pydantic schemas for the OpenClaw ↔ FredOS session bridge."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IngestTurnRequest(BaseModel):
    """Payload sent by the FredOS plugin's agent_end hook."""

    openclaw_session_id: str
    openclaw_session_key: str
    openclaw_agent_id: str
    project_id: Optional[int] = None
    user_message: str
    assistant_message: str
    tool_calls: Optional[list[dict]] = None
    duration_ms: Optional[int] = None
    success: bool = True


class IngestSummaryRequest(BaseModel):
    """Payload sent by the FredOS plugin's after_compaction hook."""

    openclaw_session_id: str
    openclaw_session_key: str
    openclaw_agent_id: str
    project_id: Optional[int] = None
    summary_text: str
    message_count: int = 0
    compacted_count: int = 0


class FinalizeSessionRequest(BaseModel):
    """Payload sent by the FredOS plugin's before_reset hook."""

    openclaw_session_id: str
    openclaw_session_key: str
    openclaw_agent_id: str
    project_id: Optional[int] = None
    reason: str = "reset"  # "reset" | "new" | "session_end"


class BridgeSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: Optional[str] = None
    status: str
    openclaw_session_id: Optional[str] = None
    openclaw_session_key: Optional[str] = None
    openclaw_agent_id: Optional[str] = None
    created_at: dt.datetime


class IngestTurnResponse(BaseModel):
    fredos_session_id: int
    memory_item_id: int
    status: str = "ingested"


class IngestSummaryResponse(BaseModel):
    fredos_session_id: int
    summary_id: int
    status: str = "summary_stored"


class FinalizeSessionResponse(BaseModel):
    fredos_session_id: int
    consolidation_result: dict
    status: str = "finalized"
