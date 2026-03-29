"""DailyBrief model — §8.14."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DailyBrief(Base):
    __tablename__ = "daily_briefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brief_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    top_priorities: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    blocked_items: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    followups: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    generated_by: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<DailyBrief id={self.id} date={self.brief_date}>"
