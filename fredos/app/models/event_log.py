"""EventLog model — System Intelligence Layer (Phase 7)."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class EventLog(Base):
    __tablename__ = "event_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "task_created", "agent_called"
    actor: Mapped[str] = mapped_column(String(255), nullable=False)       # agent or user
    payload: Mapped[Optional[str]] = mapped_column(Text)                  # JSON string
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<EventLog id={self.id} type={self.event_type!r} actor={self.actor!r}>"
