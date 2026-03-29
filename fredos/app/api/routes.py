"""API routes — aggregate all resource routers."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from app.db import get_db
from app.schemas import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    ProjectSnapshotCreate,
    ProjectSnapshotRead,
    TaskCreate,
    TaskRead,
    TaskUpdate,
    SessionCreate,
    SessionRead,
    SessionSummaryCreate,
    SessionSummaryRead,
    ResearchNoteCreate,
    ResearchNoteRead,
    DecisionCreate,
    DecisionRead,
    MemoryItemCreate,
    MemoryItemRead,
    MemoryLinkCreate,
    MemoryLinkRead,
    StructuredWriteRequest,
    StructuredWriteResponse,
    TaskMutationRequest,
    EntityLinkRequest,
)
from app.services import (
    project_service,
    task_service,
    memory_service,
    research_service,
    decision_service,
    retrieval_service,
    consolidation_service,
    fredos_service_layer,
)
from app.models.session import Session, SessionSummary

router = APIRouter()


# ══════════════════════════════════════════════════════════════
#  Projects
# ══════════════════════════════════════════════════════════════

@router.post("/projects", response_model=ProjectRead, tags=["Projects"])
def create_project(body: ProjectCreate, db: DBSession = Depends(get_db)):
    return project_service.create_project(db, **body.model_dump())


@router.get("/projects", response_model=list[ProjectRead], tags=["Projects"])
def list_projects(
    status: Optional[str] = None,
    client_name: Optional[str] = None,
    db: DBSession = Depends(get_db),
):
    return project_service.list_projects(db, status=status, client_name=client_name)


@router.get("/projects/{project_id}", response_model=ProjectRead, tags=["Projects"])
def get_project(project_id: int, db: DBSession = Depends(get_db)):
    p = project_service.get_project(db, project_id)
    if p is None:
        raise HTTPException(404, "Project not found")
    return p


@router.patch("/projects/{project_id}", response_model=ProjectRead, tags=["Projects"])
def update_project(
    project_id: int, body: ProjectUpdate, db: DBSession = Depends(get_db)
):
    p = project_service.update_project(
        db, project_id, **body.model_dump(exclude_unset=True)
    )
    if p is None:
        raise HTTPException(404, "Project not found")
    return p


@router.delete("/projects/{project_id}", tags=["Projects"])
def delete_project(project_id: int, db: DBSession = Depends(get_db)):
    if not project_service.delete_project(db, project_id):
        raise HTTPException(404, "Project not found")
    return {"deleted": True}


# ── Project Snapshots ─────────────────────────────────────────

@router.post("/projects/{project_id}/snapshots", response_model=ProjectSnapshotRead, tags=["Projects"])
def create_snapshot(
    project_id: int, body: ProjectSnapshotCreate, db: DBSession = Depends(get_db)
):
    return project_service.create_snapshot(db, project_id=project_id, **body.model_dump(exclude={"project_id"}))


@router.get("/projects/{project_id}/snapshots", response_model=list[ProjectSnapshotRead], tags=["Projects"])
def list_snapshots(project_id: int, db: DBSession = Depends(get_db)):
    return project_service.list_snapshots(db, project_id)


# ══════════════════════════════════════════════════════════════
#  Tasks
# ══════════════════════════════════════════════════════════════

@router.post("/tasks", response_model=TaskRead, tags=["Tasks"])
def create_task(body: TaskCreate, db: DBSession = Depends(get_db)):
    return task_service.create_task(db, **body.model_dump())


@router.get("/tasks", response_model=list[TaskRead], tags=["Tasks"])
def list_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    db: DBSession = Depends(get_db),
):
    return task_service.list_tasks(db, project_id=project_id, status=status)


@router.get("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def get_task(task_id: int, db: DBSession = Depends(get_db)):
    t = task_service.get_task(db, task_id)
    if t is None:
        raise HTTPException(404, "Task not found")
    return t


@router.patch("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def update_task(task_id: int, body: TaskUpdate, db: DBSession = Depends(get_db)):
    t = task_service.update_task(db, task_id, **body.model_dump(exclude_unset=True))
    if t is None:
        raise HTTPException(404, "Task not found")
    return t


@router.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: DBSession = Depends(get_db)):
    if not task_service.delete_task(db, task_id):
        raise HTTPException(404, "Task not found")
    return {"deleted": True}


# ══════════════════════════════════════════════════════════════
#  Sessions
# ══════════════════════════════════════════════════════════════

@router.post("/sessions", response_model=SessionRead, tags=["Sessions"])
def create_session(body: SessionCreate, db: DBSession = Depends(get_db)):
    s = Session(**body.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/sessions", response_model=list[SessionRead], tags=["Sessions"])
def list_sessions(
    project_id: Optional[int] = None, db: DBSession = Depends(get_db)
):
    q = db.query(Session)
    if project_id is not None:
        q = q.filter(Session.project_id == project_id)
    return q.order_by(Session.created_at.desc()).all()


@router.get("/sessions/{session_id}", response_model=SessionRead, tags=["Sessions"])
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    s = db.get(Session, session_id)
    if s is None:
        raise HTTPException(404, "Session not found")
    return s


# ── Session Summaries ─────────────────────────────────────────

@router.post("/sessions/{session_id}/summaries", response_model=SessionSummaryRead, tags=["Sessions"])
def create_session_summary(
    session_id: int, body: SessionSummaryCreate, db: DBSession = Depends(get_db)
):
    ss = SessionSummary(session_id=session_id, **body.model_dump(exclude={"session_id"}))
    db.add(ss)
    db.commit()
    db.refresh(ss)
    return ss


# ══════════════════════════════════════════════════════════════
#  Research Notes
# ══════════════════════════════════════════════════════════════

@router.post("/research-notes", response_model=ResearchNoteRead, tags=["Research"])
def create_research_note(body: ResearchNoteCreate, db: DBSession = Depends(get_db)):
    return research_service.create_research_note(db, **body.model_dump())


@router.get("/research-notes", response_model=list[ResearchNoteRead], tags=["Research"])
def list_research_notes(
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    db: DBSession = Depends(get_db),
):
    return research_service.list_research_notes(db, project_id=project_id, task_id=task_id)


# ══════════════════════════════════════════════════════════════
#  Decisions
# ══════════════════════════════════════════════════════════════

@router.post("/decisions", response_model=DecisionRead, tags=["Decisions"])
def create_decision(body: DecisionCreate, db: DBSession = Depends(get_db)):
    return decision_service.create_decision(db, **body.model_dump())


@router.get("/decisions", response_model=list[DecisionRead], tags=["Decisions"])
def list_decisions(
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    db: DBSession = Depends(get_db),
):
    return decision_service.list_decisions(db, project_id=project_id, task_id=task_id)


# ══════════════════════════════════════════════════════════════
#  Memory
# ══════════════════════════════════════════════════════════════

@router.post("/memory/items", response_model=MemoryItemRead, tags=["Memory"])
def create_memory_item(body: MemoryItemCreate, db: DBSession = Depends(get_db)):
    return memory_service.create_memory_item(db, **body.model_dump())


@router.get("/memory/items", response_model=list[MemoryItemRead], tags=["Memory"])
def list_memory_items(
    project_id: Optional[int] = None,
    memory_level: Optional[str] = None,
    db: DBSession = Depends(get_db),
):
    return memory_service.list_memory_items(
        db, project_id=project_id, memory_level=memory_level
    )


@router.post("/memory/links", response_model=MemoryLinkRead, tags=["Memory"])
def create_memory_link(body: MemoryLinkCreate, db: DBSession = Depends(get_db)):
    return memory_service.create_memory_link(db, **body.model_dump())


# ══════════════════════════════════════════════════════════════
#  Retrieval
# ══════════════════════════════════════════════════════════════

@router.get("/retrieve/project-overview/{project_id}", tags=["Retrieval"])
def retrieve_project_overview(project_id: int, db: DBSession = Depends(get_db)):
    return retrieval_service.retrieve_project_overview(db, project_id)


@router.get("/retrieve/task-support/{task_id}", tags=["Retrieval"])
def retrieve_task_support(task_id: int, db: DBSession = Depends(get_db)):
    return retrieval_service.retrieve_task_support(db, task_id)


@router.get("/retrieve/research/{project_id}", tags=["Retrieval"])
def retrieve_research(project_id: int, db: DBSession = Depends(get_db)):
    return retrieval_service.retrieve_research(db, project_id)


@router.get("/retrieve/personal-strategy", tags=["Retrieval"])
def retrieve_personal_strategy(db: DBSession = Depends(get_db)):
    return retrieval_service.retrieve_personal_strategy(db)


# ══════════════════════════════════════════════════════════════
#  Consolidation
# ══════════════════════════════════════════════════════════════

@router.post("/consolidate/{session_id}", tags=["Consolidation"])
def consolidate_session(session_id: int, db: DBSession = Depends(get_db)):
    result = consolidation_service.consolidate_session(db, session_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result


@router.post(
    "/fredos/write-structured",
    response_model=StructuredWriteResponse,
    tags=["FredOS Service Layer"],
)
def fredos_write_structured(
    body: StructuredWriteRequest, db: DBSession = Depends(get_db)
):
    return fredos_service_layer.write_structured(db, **body.model_dump())


@router.patch(
    "/fredos/tasks/{task_id}",
    response_model=StructuredWriteResponse,
    tags=["FredOS Service Layer"],
)
def fredos_update_task(
    task_id: int, body: TaskMutationRequest, db: DBSession = Depends(get_db)
):
    return fredos_service_layer.update_task_structured(
        db, task_id, **body.model_dump(exclude_unset=True)
    )


@router.post(
    "/fredos/link-entities",
    response_model=StructuredWriteResponse,
    tags=["FredOS Service Layer"],
)
def fredos_link_entities(
    body: EntityLinkRequest, db: DBSession = Depends(get_db)
):
    return fredos_service_layer.link_entities(db, **body.model_dump())
