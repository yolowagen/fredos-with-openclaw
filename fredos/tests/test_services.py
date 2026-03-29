"""Tests — service-layer round-trip tests."""

import sys
import os
import json

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.services import (
    project_service,
    task_service,
    memory_service,
    research_service,
    decision_service,
    consolidation_service,
    fredos_service_layer,
)

TEST_ENGINE = create_engine("sqlite:///:memory:")
TestSession = sessionmaker(bind=TEST_ENGINE)


@pytest.fixture()
def db():
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=TEST_ENGINE)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=TEST_ENGINE)


# ── Project service ───────────────────────────────────────────

def test_create_and_get_project(db):
    p = project_service.create_project(db, name="TestProject", client_name="Acme")
    assert p.id is not None
    assert p.name == "TestProject"

    fetched = project_service.get_project(db, p.id)
    assert fetched is not None
    assert fetched.name == "TestProject"


def test_list_projects_filter(db):
    project_service.create_project(db, name="A", status="active")
    project_service.create_project(db, name="B", status="archived")
    active = project_service.list_projects(db, status="active")
    assert len(active) == 1
    assert active[0].name == "A"


def test_update_project(db):
    p = project_service.create_project(db, name="Old")
    updated = project_service.update_project(db, p.id, name="New")
    assert updated.name == "New"


def test_delete_project(db):
    p = project_service.create_project(db, name="Doomed")
    assert project_service.delete_project(db, p.id) is True
    assert project_service.get_project(db, p.id) is None


# ── Task service ──────────────────────────────────────────────

def test_create_task(db):
    p = project_service.create_project(db, name="P")
    t = task_service.create_task(db, project_id=p.id, title="Do stuff")
    assert t.id is not None
    assert t.title == "Do stuff"


def test_list_tasks_by_project(db):
    p1 = project_service.create_project(db, name="P1")
    p2 = project_service.create_project(db, name="P2")
    task_service.create_task(db, project_id=p1.id, title="T1")
    task_service.create_task(db, project_id=p2.id, title="T2")
    tasks = task_service.list_tasks(db, project_id=p1.id)
    assert len(tasks) == 1
    assert tasks[0].title == "T1"


# ── Memory service ────────────────────────────────────────────

def test_create_memory_item(db):
    mi = memory_service.create_memory_item(
        db, memory_level="L2", content="A decision was made"
    )
    assert mi.id is not None
    assert mi.memory_level == "L2"


def test_create_memory_link(db):
    m1 = memory_service.create_memory_item(db, memory_level="L2", content="A")
    m2 = memory_service.create_memory_item(db, memory_level="L2", content="B")
    link = memory_service.create_memory_link(
        db, from_memory_id=m1.id, to_memory_id=m2.id, relation_type="related"
    )
    assert link.id is not None


# ── Research service ──────────────────────────────────────────

def test_create_research_note(db):
    p = project_service.create_project(db, name="P")
    note = research_service.create_research_note(
        db, project_id=p.id, title="Root cause analysis"
    )
    assert note.id is not None


# ── Decision service ──────────────────────────────────────────

def test_create_decision(db):
    p = project_service.create_project(db, name="P")
    d = decision_service.create_decision(
        db, project_id=p.id, title="Use SQLite for v0.1"
    )
    assert d.id is not None


# ── Consolidation service ────────────────────────────────────

def test_consolidate_session(db):
    from app.models.session import Session, SessionSummary

    p = project_service.create_project(db, name="P")
    s = Session(project_id=p.id, title="Work session 1", status="active")
    db.add(s)
    db.commit()
    db.refresh(s)

    ss = SessionSummary(
        session_id=s.id,
        summary="Investigated speaker failure modes",
        extracted_tasks=json.dumps(["Check vibration data", "Review THD results"]),
    )
    db.add(ss)
    db.commit()

    result = consolidation_service.consolidate_session(db, s.id)
    assert result["status"] == "consolidated"
    assert len(result["created"]["memory_items"]) >= 1
    assert result["created"]["snapshot"] is not None

    # Verify idempotency.
    result2 = consolidation_service.consolidate_session(db, s.id)
    assert result2.get("info") == "Session already consolidated"


def test_structured_write_knowledge(db):
    p = project_service.create_project(db, name="P")
    result = fredos_service_layer.write_structured(
        db,
        record_type="knowledge",
        project_id=p.id,
        title="Research finding",
        author_agent="operator-agent",
        rationale="Need durable research capture",
        summary="The plugin should use wrapper endpoints.",
    )
    assert result["record_type"] == "knowledge"
    assert result["status"] == "created"


def test_structured_task_update_requires_fields(db):
    p = project_service.create_project(db, name="P")
    task = task_service.create_task(db, project_id=p.id, title="Do thing")
    result = fredos_service_layer.update_task_structured(
        db,
        task.id,
        author_agent="operator-agent",
        rationale="Task has started",
        status="in_progress",
    )
    assert result["status"] == "updated"


def test_link_entities_supports_memory_links(db):
    p = project_service.create_project(db, name="P")
    left = memory_service.create_memory_item(db, memory_level="L2", project_id=p.id, content="A")
    right = memory_service.create_memory_item(db, memory_level="L2", project_id=p.id, content="B")
    result = fredos_service_layer.link_entities(
        db,
        author_agent="memory-manager-agent",
        relation_type="related",
        from_memory_id=left.id,
        to_memory_id=right.id,
        project_id=p.id,
        rationale="Both memories describe the same subsystem.",
    )
    assert result["record_type"] == "memory_link"
    assert result["status"] == "created"
