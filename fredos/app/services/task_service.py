"""Task service — CRUD for tasks and task dependencies."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session as DBSession

from app.models.task import Task, TaskDependency


# ── Tasks ─────────────────────────────────────────────────────

def create_task(db: DBSession, **kwargs) -> Task:
    task = Task(**kwargs)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: DBSession, task_id: int) -> Optional[Task]:
    return db.get(Task, task_id)


def list_tasks(
    db: DBSession,
    *,
    project_id: Optional[int] = None,
    status: Optional[str] = None,
) -> list[Task]:
    q = db.query(Task)
    if project_id is not None:
        q = q.filter(Task.project_id == project_id)
    if status:
        q = q.filter(Task.status == status)
    return q.order_by(Task.updated_at.desc()).all()


def update_task(db: DBSession, task_id: int, **kwargs) -> Optional[Task]:
    task = db.get(Task, task_id)
    if task is None:
        return None
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: DBSession, task_id: int) -> bool:
    task = db.get(Task, task_id)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True


# ── Task Dependencies ─────────────────────────────────────────

def add_dependency(
    db: DBSession,
    task_id: int,
    depends_on_task_id: int,
    dependency_type: Optional[str] = None,
) -> TaskDependency:
    dep = TaskDependency(
        task_id=task_id,
        depends_on_task_id=depends_on_task_id,
        dependency_type=dependency_type,
    )
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return dep


def list_dependencies(db: DBSession, task_id: int) -> list[TaskDependency]:
    return (
        db.query(TaskDependency)
        .filter(TaskDependency.task_id == task_id)
        .all()
    )
