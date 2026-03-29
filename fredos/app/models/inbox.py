"""InboxItem model — §8.12."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class InboxItem(Base):
    __tablename__ = "inbox_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_type: Mapped[Optional[str]] = mapped_column(String(100))
    source_ref: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(String(500))
    raw_content: Mapped[Optional[str]] = mapped_column(Text)
    normalized_summary: Mapped[Optional[str]] = mapped_column(Text)
    linked_project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id")
    )
    linked_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))
    status: Mapped[str] = mapped_column(String(50), default="new")
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<InboxItem id={self.id} title={self.title!r}>"
