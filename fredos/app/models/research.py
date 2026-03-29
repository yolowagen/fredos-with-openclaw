"""ResearchNote model — §8.5."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResearchNote(Base):
    __tablename__ = "research_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    question: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    hypotheses: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    recommendations: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    source_refs: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<ResearchNote id={self.id} title={self.title!r}>"


class Decision(Base):
    """Decision model — §8.6."""

    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    context: Mapped[Optional[str]] = mapped_column(Text)
    decision_made: Mapped[Optional[str]] = mapped_column(Text)
    reasoning_summary: Mapped[Optional[str]] = mapped_column(Text)
    tradeoffs: Mapped[Optional[str]] = mapped_column(Text)
    decided_by: Mapped[Optional[str]] = mapped_column(String(100))
    decided_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Decision id={self.id} title={self.title!r}>"
