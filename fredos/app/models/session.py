"""Session and SessionSummary models — §8.7, §8.8."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default="active")
    goal: Mapped[Optional[str]] = mapped_column(Text)
    openclaw_session_id: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True, index=True, unique=True
    )
    openclaw_session_key: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, index=True
    )
    openclaw_agent_id: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )
    started_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    ended_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # relationships
    summaries: Mapped[list["SessionSummary"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Session id={self.id} title={self.title!r}>"


class SessionSummary(Base):
    __tablename__ = "session_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"), nullable=False
    )
    summary: Mapped[Optional[str]] = mapped_column(Text)
    open_loops: Mapped[Optional[str]] = mapped_column(Text)
    extracted_tasks: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    extracted_decisions: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    session: Mapped["Session"] = relationship(back_populates="summaries")

    def __repr__(self) -> str:
        return f"<SessionSummary id={self.id} session_id={self.session_id}>"
