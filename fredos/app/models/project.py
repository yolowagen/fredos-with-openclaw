"""Project and ProjectSnapshot models — §8.1, §8.2."""

from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_name: Mapped[Optional[str]] = mapped_column(String(255))
    role_title: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="active")
    priority: Mapped[Optional[str]] = mapped_column(String(50))
    objective: Mapped[Optional[str]] = mapped_column(Text)
    current_state: Mapped[Optional[str]] = mapped_column(Text)
    current_phase: Mapped[Optional[str]] = mapped_column(String(100))
    major_risks: Mapped[Optional[str]] = mapped_column(Text)
    next_actions: Mapped[Optional[str]] = mapped_column(Text)
    domain_tags: Mapped[Optional[str]] = mapped_column(Text)  # JSON-encoded list
    related_links: Mapped[Optional[str]] = mapped_column(Text)  # JSON-encoded list
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # relationships
    snapshots: Mapped[list["ProjectSnapshot"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name!r}>"


class ProjectSnapshot(Base):
    __tablename__ = "project_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    open_questions: Mapped[Optional[str]] = mapped_column(Text)
    key_changes: Mapped[Optional[str]] = mapped_column(Text)
    blockers: Mapped[Optional[str]] = mapped_column(Text)
    recommended_focus: Mapped[Optional[str]] = mapped_column(Text)
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    project: Mapped["Project"] = relationship(back_populates="snapshots")

    def __repr__(self) -> str:
        return f"<ProjectSnapshot id={self.id} project_id={self.project_id}>"
