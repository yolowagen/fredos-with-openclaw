"""ExecutionRun model — §8.13."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ExecutionRun(Base):
    __tablename__ = "execution_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"))
    adapter_name: Mapped[Optional[str]] = mapped_column(String(100))
    command_name: Mapped[Optional[str]] = mapped_column(String(255))
    input_payload: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    stdout_log: Mapped[Optional[str]] = mapped_column(Text)
    stderr_log: Mapped[Optional[str]] = mapped_column(Text)
    result_summary: Mapped[Optional[str]] = mapped_column(Text)
    artifact_paths: Mapped[Optional[str]] = mapped_column(Text)  # JSON-encoded list
    started_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    finished_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<ExecutionRun id={self.id} status={self.status}>"
