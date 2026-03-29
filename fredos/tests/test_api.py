"""Tests — API smoke tests using FastAPI TestClient."""

import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base, get_db
from app.main import app

# Use in-memory SQLite for API tests.
TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=TEST_ENGINE)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


# ── Health ────────────────────────────────────────────────────

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── Projects CRUD ─────────────────────────────────────────────

def test_create_project():
    r = client.post("/api/projects", json={"name": "Phrozen", "client_name": "Phrozen Technology"})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Phrozen"
    assert data["id"] is not None


def test_list_projects():
    client.post("/api/projects", json={"name": "A"})
    client.post("/api/projects", json={"name": "B"})
    r = client.get("/api/projects")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_project():
    r = client.post("/api/projects", json={"name": "X"})
    pid = r.json()["id"]
    r2 = client.get(f"/api/projects/{pid}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "X"


def test_update_project():
    r = client.post("/api/projects", json={"name": "Old"})
    pid = r.json()["id"]
    r2 = client.patch(f"/api/projects/{pid}", json={"name": "New"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "New"


def test_delete_project():
    r = client.post("/api/projects", json={"name": "Bye"})
    pid = r.json()["id"]
    r2 = client.delete(f"/api/projects/{pid}")
    assert r2.status_code == 200
    r3 = client.get(f"/api/projects/{pid}")
    assert r3.status_code == 404


# ── Tasks CRUD ────────────────────────────────────────────────

def test_create_task():
    p = client.post("/api/projects", json={"name": "P"}).json()
    r = client.post("/api/tasks", json={"project_id": p["id"], "title": "Do it"})
    assert r.status_code == 200
    assert r.json()["title"] == "Do it"


# ── Sessions ──────────────────────────────────────────────────

def test_create_session():
    p = client.post("/api/projects", json={"name": "P"}).json()
    r = client.post("/api/sessions", json={"project_id": p["id"], "title": "Session 1"})
    assert r.status_code == 200


# ── Research Notes ────────────────────────────────────────────

def test_create_research_note():
    p = client.post("/api/projects", json={"name": "P"}).json()
    r = client.post(
        "/api/research-notes",
        json={"project_id": p["id"], "title": "Root cause"},
    )
    assert r.status_code == 200


# ── Decisions ─────────────────────────────────────────────────

def test_create_decision():
    p = client.post("/api/projects", json={"name": "P"}).json()
    r = client.post(
        "/api/decisions",
        json={"project_id": p["id"], "title": "Use SQLite"},
    )
    assert r.status_code == 200


# ── Retrieval ─────────────────────────────────────────────────

def test_retrieve_project_overview():
    p = client.post("/api/projects", json={"name": "P"}).json()
    r = client.get(f"/api/retrieve/project-overview/{p['id']}")
    assert r.status_code == 200
    assert r.json()["mode"] == "A"


def test_retrieve_personal_strategy():
    r = client.get("/api/retrieve/personal-strategy")
    assert r.status_code == 200
    assert r.json()["mode"] == "D"


def test_retrieve_task_support():
    p = client.post("/api/projects", json={"name": "P"}).json()
    task = client.post("/api/tasks", json={"project_id": p["id"], "title": "Do it"}).json()
    r = client.get(f"/api/retrieve/task-support/{task['id']}")
    assert r.status_code == 200
    assert r.json()["mode"] == "B"


# ── Consolidation ─────────────────────────────────────────────

def test_consolidation_flow():
    p = client.post("/api/projects", json={"name": "P"}).json()
    s = client.post(
        "/api/sessions",
        json={"project_id": p["id"], "title": "Work"},
    ).json()
    client.post(
        f"/api/sessions/{s['id']}/summaries",
        json={"session_id": s["id"], "summary": "Did some research"},
    )
    r = client.post(f"/api/consolidate/{s['id']}")
    assert r.status_code == 200
    assert r.json()["status"] == "consolidated"


def test_fredos_write_structured():
    p = client.post("/api/projects", json={"name": "P"}).json()
    r = client.post(
        "/api/fredos/write-structured",
        json={
            "record_type": "knowledge",
            "project_id": p["id"],
            "title": "Wrapped write",
            "author_agent": "operator-agent",
            "rationale": "Persist a durable note",
            "summary": "Structured wrapper works.",
        },
    )
    assert r.status_code == 200
    assert r.json()["record_type"] == "knowledge"


def test_fredos_update_task():
    p = client.post("/api/projects", json={"name": "P"}).json()
    task = client.post("/api/tasks", json={"project_id": p["id"], "title": "Do it"}).json()
    r = client.patch(
        f"/api/fredos/tasks/{task['id']}",
        json={
            "author_agent": "operator-agent",
            "rationale": "Work has started",
            "status": "in_progress",
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "updated"


def test_fredos_link_entities():
    p = client.post("/api/projects", json={"name": "P"}).json()
    left = client.post(
        "/api/memory/items",
        json={"memory_level": "L2", "project_id": p["id"], "content": "A"},
    ).json()
    right = client.post(
        "/api/memory/items",
        json={"memory_level": "L2", "project_id": p["id"], "content": "B"},
    ).json()
    r = client.post(
        "/api/fredos/link-entities",
        json={
            "author_agent": "memory-manager-agent",
            "relation_type": "related",
            "from_memory_id": left["id"],
            "to_memory_id": right["id"],
            "project_id": p["id"],
            "rationale": "These memory items belong together",
        },
    )
    assert r.status_code == 200
    assert r.json()["record_type"] == "memory_link"
