"""Tests for model/table creation sanity checks."""

import os
import sys

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.base import Base


TEST_ENGINE = create_engine("sqlite:///:memory:")
TestSession = sessionmaker(bind=TEST_ENGINE)


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test, then tear them down."""
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


EXPECTED_TABLES = [
    "projects",
    "project_snapshots",
    "tasks",
    "task_dependencies",
    "sessions",
    "session_summaries",
    "research_notes",
    "decisions",
    "memory_items",
    "memory_links",
    "documents",
    "inbox_items",
    "execution_runs",
    "daily_briefs",
    "event_logs",
]


def test_all_tables_created():
    inspector = inspect(TEST_ENGINE)
    tables = inspector.get_table_names()
    for name in EXPECTED_TABLES:
        assert name in tables, f"Missing table: {name}"


def test_table_count():
    inspector = inspect(TEST_ENGINE)
    tables = inspector.get_table_names()
    assert len(tables) == len(EXPECTED_TABLES), (
        f"Expected {len(EXPECTED_TABLES)} tables, got {len(tables)}: {tables}"
    )
