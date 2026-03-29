"""Pydantic schemas for API request/response validation."""

from __future__ import annotations

import datetime as dt
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


# ──────────────────────────────────────────────────────────────
# Project
# ──────────────────────────────────────────────────────────────
class ProjectBase(BaseModel):
    name: str
    client_name: Optional[str] = None
    role_title: Optional[str] = None
    status: str = "active"
    priority: Optional[str] = None
    objective: Optional[str] = None
    current_state: Optional[str] = None
    current_phase: Optional[str] = None
    major_risks: Optional[str] = None
    next_actions: Optional[str] = None
    domain_tags: Optional[str] = None
    related_links: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_name: Optional[str] = None
    role_title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    objective: Optional[str] = None
    current_state: Optional[str] = None
    current_phase: Optional[str] = None
    major_risks: Optional[str] = None
    next_actions: Optional[str] = None
    domain_tags: Optional[str] = None
    related_links: Optional[str] = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime
    updated_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# ProjectSnapshot
# ──────────────────────────────────────────────────────────────
class ProjectSnapshotCreate(BaseModel):
    project_id: int
    summary: Optional[str] = None
    open_questions: Optional[str] = None
    key_changes: Optional[str] = None
    blockers: Optional[str] = None
    recommended_focus: Optional[str] = None
    created_by: Optional[str] = None


class ProjectSnapshotRead(ProjectSnapshotCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# Task
# ──────────────────────────────────────────────────────────────
class TaskBase(BaseModel):
    project_id: int
    parent_task_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "open"
    priority: Optional[str] = None
    task_type: Optional[str] = None
    owner_type: Optional[str] = None
    owner_name: Optional[str] = None
    needs_research: bool = False
    needs_execution: bool = False
    due_at: Optional[dt.datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    task_type: Optional[str] = None
    owner_type: Optional[str] = None
    owner_name: Optional[str] = None
    needs_research: Optional[bool] = None
    needs_execution: Optional[bool] = None
    due_at: Optional[dt.datetime] = None
    started_at: Optional[dt.datetime] = None
    completed_at: Optional[dt.datetime] = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    started_at: Optional[dt.datetime] = None
    completed_at: Optional[dt.datetime] = None
    created_at: dt.datetime
    updated_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# Session
# ──────────────────────────────────────────────────────────────
class SessionBase(BaseModel):
    project_id: int
    title: Optional[str] = None
    status: str = "active"
    goal: Optional[str] = None


class SessionCreate(SessionBase):
    pass


class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    started_at: Optional[dt.datetime] = None
    ended_at: Optional[dt.datetime] = None
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# SessionSummary
# ──────────────────────────────────────────────────────────────
class SessionSummaryCreate(BaseModel):
    session_id: int
    summary: Optional[str] = None
    open_loops: Optional[str] = None
    extracted_tasks: Optional[str] = None
    extracted_decisions: Optional[str] = None


class SessionSummaryRead(SessionSummaryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# ResearchNote
# ──────────────────────────────────────────────────────────────
class ResearchNoteCreate(BaseModel):
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    title: str
    question: Optional[str] = None
    summary: Optional[str] = None
    hypotheses: Optional[str] = None
    recommendations: Optional[str] = None
    source_refs: Optional[str] = None
    created_by: Optional[str] = None


class ResearchNoteRead(ResearchNoteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# Decision
# ──────────────────────────────────────────────────────────────
class DecisionCreate(BaseModel):
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    title: str
    context: Optional[str] = None
    decision_made: Optional[str] = None
    reasoning_summary: Optional[str] = None
    tradeoffs: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[dt.datetime] = None


class DecisionRead(DecisionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# MemoryItem
# ──────────────────────────────────────────────────────────────
class MemoryItemCreate(BaseModel):
    memory_level: str  # L0, L1, L2, L3, L4
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    session_id: Optional[int] = None
    source_type: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    importance_score: Optional[float] = None
    sensitivity: Optional[str] = None


class MemoryItemRead(MemoryItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# MemoryLink
# ──────────────────────────────────────────────────────────────
class MemoryLinkCreate(BaseModel):
    from_memory_id: int
    to_memory_id: int
    relation_type: Optional[str] = None


class MemoryLinkRead(MemoryLinkCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


# ──────────────────────────────────────────────────────────────
# Document
# ──────────────────────────────────────────────────────────────
class DocumentCreate(BaseModel):
    project_id: Optional[int] = None
    title: str
    doc_type: Optional[str] = None
    source_type: Optional[str] = None
    source_uri: Optional[str] = None
    artifact_path: Optional[str] = None
    content_text: Optional[str] = None
    content_summary: Optional[str] = None
    tags: Optional[str] = None


class DocumentRead(DocumentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime
    updated_at: dt.datetime


class StructuredWriteRequest(BaseModel):
    record_type: Literal["task", "decision", "knowledge"]
    project_id: int
    title: str
    author_agent: str
    rationale: Optional[str] = None
    task_id: Optional[int] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    recommendations: Optional[str] = None
    confidence: Optional[float] = None
    source_refs: Optional[str] = None


class StructuredWriteResponse(BaseModel):
    record_type: str
    record_id: int
    project_id: int
    status: str


class TaskMutationRequest(BaseModel):
    author_agent: str
    rationale: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    owner_type: Optional[str] = None
    owner_name: Optional[str] = None
    needs_research: Optional[bool] = None
    needs_execution: Optional[bool] = None
    started_at: Optional[dt.datetime] = None
    completed_at: Optional[dt.datetime] = None


class EntityLinkRequest(BaseModel):
    author_agent: str
    relation_type: str
    from_memory_id: Optional[int] = None
    to_memory_id: Optional[int] = None
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    rationale: Optional[str] = None
