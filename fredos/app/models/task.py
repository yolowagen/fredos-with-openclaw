"""Task and TaskDependency models — §8.3, §8.4."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    parent_task_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tasks.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="open")
    priority: Mapped[Optional[str]] = mapped_column(String(50))
    task_type: Mapped[Optional[str]] = mapped_column(String(100))
    owner_type: Mapped[Optional[str]] = mapped_column(String(50))  # "agent" | "human"
    owner_name: Mapped[Optional[str]] = mapped_column(String(255))
    needs_research: Mapped[bool] = mapped_column(default=False)
    needs_execution: Mapped[bool] = mapped_column(default=False)
    due_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    started_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[dt.datetime]] = mapped_column(DateTime)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # relationships
    subtasks: Mapped[list["Task"]] = relationship(
        back_populates="parent_task", cascade="all, delete-orphan"
    )
    parent_task: Mapped[Optional["Task"]] = relationship(
        back_populates="subtasks", remote_side=[id]
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r}>"


class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    depends_on_task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"), nullable=False
    )
    dependency_type: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<TaskDependency {self.task_id} -> {self.depends_on_task_id}>"
