"""SQLAlchemy engine, session factory, and declarative Base."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core import settings


# ── Engine ────────────────────────────────────────────────────
# check_same_thread is only needed for SQLite.
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args=connect_args,
)

# ── Session factory ───────────────────────────────────────────
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """FastAPI dependency — yields a DB session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Declarative base ─────────────────────────────────────────
class Base(DeclarativeBase):
    """Shared declarative base for all FredOS models."""
    pass
