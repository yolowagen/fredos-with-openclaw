"""MemoryItem and MemoryLink models — §8.9, §8.10."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MemoryItem(Base):
    __tablename__ = "memory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    memory_level: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # L0, L1, L2, L3, L4
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))
    session_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sessions.id"))
    source_type: Mapped[Optional[str]] = mapped_column(String(100))
    content: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    importance_score: Mapped[Optional[float]] = mapped_column(Float, default=0.5)
    last_accessed_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    decay_factor: Mapped[Optional[float]] = mapped_column(Float, default=0.01)
    sensitivity: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<MemoryItem id={self.id} level={self.memory_level}>"


class MemoryLink(Base):
    __tablename__ = "memory_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_memory_id: Mapped[int] = mapped_column(
        ForeignKey("memory_items.id"), nullable=False
    )
    to_memory_id: Mapped[int] = mapped_column(
        ForeignKey("memory_items.id"), nullable=False
    )
    relation_type: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<MemoryLink {self.from_memory_id} -[{self.relation_type}]-> {self.to_memory_id}>"
