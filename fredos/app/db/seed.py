"""Seed the database with initial projects: Phrozen and Otowahr."""

from __future__ import annotations

from sqlalchemy.orm import Session as DBSession

from app.db.base import SessionLocal, engine, Base
from app.models import Project, Task


def seed():
    """Create tables (if needed) and insert seed data."""
    # Import all models so Base.metadata knows every table.
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    db: DBSession = SessionLocal()
    try:
        # Only seed if no projects exist yet.
        if db.query(Project).count() > 0:
            print("Database already seeded — skipping.")
            return

        # ── Project: Phrozen ──────────────────────────────────
        phrozen = Project(
            name="Phrozen",
            client_name="Phrozen Technology",
            role_title="Engineering Consultant",
            status="active",
            priority="high",
            objective="Design and optimise workflow for Phrozen product line",
            current_state="Active development",
            current_phase="Phase 2 — Workflow Optimisation",
            domain_tags='["3D printing", "manufacturing", "workflow"]',
        )
        db.add(phrozen)
        db.flush()  # get phrozen.id

        db.add(
            Task(
                project_id=phrozen.id,
                title="Review current workflow documentation",
                status="open",
                priority="high",
                task_type="research",
                owner_type="human",
                owner_name="Fred",
                needs_research=True,
            )
        )

        # ── Project: Otowahr ──────────────────────────────────
        otowahr = Project(
            name="Otowahr",
            client_name="Otowahr Audio",
            role_title="Engineering Consultant",
            status="active",
            priority="high",
            objective="Investigate and resolve micro-speaker quality issues",
            current_state="Active investigation",
            current_phase="Phase 1 — Root Cause Analysis",
            domain_tags='["audio", "micro-speakers", "quality"]',
        )
        db.add(otowahr)
        db.flush()

        db.add(
            Task(
                project_id=otowahr.id,
                title="Analyse HTOL test failure data",
                status="open",
                priority="high",
                task_type="research",
                owner_type="human",
                owner_name="Fred",
                needs_research=True,
            )
        )

        db.commit()
        print("Seeded 2 projects (Phrozen, Otowahr) with initial tasks.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
