"""Project service — CRUD for projects and project snapshots."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.project import Project, ProjectSnapshot


# ── Projects ──────────────────────────────────────────────────

def create_project(db: DBSession, **kwargs) -> Project:
    """Create and return a new project."""
    project = Project(**kwargs)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project(db: DBSession, project_id: int) -> Optional[Project]:
    """Return a project by ID, or None."""
    return db.get(Project, project_id)


def list_projects(
    db: DBSession,
    *,
    status: Optional[str] = None,
    client_name: Optional[str] = None,
) -> list[Project]:
    """List projects with optional filters."""
    q = db.query(Project)
    if status:
        q = q.filter(Project.status == status)
    if client_name:
        q = q.filter(Project.client_name == client_name)
    return q.order_by(Project.updated_at.desc()).all()


def update_project(db: DBSession, project_id: int, **kwargs) -> Optional[Project]:
    """Partially update a project.  Returns the updated object or None."""
    project = db.get(Project, project_id)
    if project is None:
        return None
    for key, value in kwargs.items():
        if hasattr(project, key):
            setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: DBSession, project_id: int) -> bool:
    """Delete a project.  Returns True if found and deleted."""
    project = db.get(Project, project_id)
    if project is None:
        return False
    db.delete(project)
    db.commit()
    return True


# ── Project Snapshots ─────────────────────────────────────────

def create_snapshot(db: DBSession, **kwargs) -> ProjectSnapshot:
    snap = ProjectSnapshot(**kwargs)
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def list_snapshots(db: DBSession, project_id: int) -> list[ProjectSnapshot]:
    return (
        db.query(ProjectSnapshot)
        .filter(ProjectSnapshot.project_id == project_id)
        .order_by(ProjectSnapshot.created_at.desc())
        .all()
    )
