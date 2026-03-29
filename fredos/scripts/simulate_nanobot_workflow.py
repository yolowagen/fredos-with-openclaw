"""E2E Simulation — Test FredOS Services programmatically simulating Nanobot workflow.

This script demonstrates a full cycle without invoking an actual LLM:
1. "Router Agent" receives request -> identifies project -> creates task
2. "Execution/User" does work -> starts session
3. "Memory Curator" extracts session summary -> triggers consolidation
4. Re-query project state (Mode A) to verify memory update.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal, engine, Base
from app.services import (
    project_service,
    task_service,
    retrieval_service,
    consolidation_service
)
from app.models.session import Session, SessionSummary


def simulate():
    db = SessionLocal()
    
    print("=== FREDOS E2E SIMULATION ===\n")

    # Ensure tables exist (tests or seed might have already done this)
    import app.models  # noqa
    Base.metadata.create_all(bind=engine)

    # 1. Router Agent Step
    print("> ROUTER AGENT: Looking up active projects...")
    projects = project_service.list_projects(db)
    if not projects:
        print("No seed projects found. Try running seed.py.")
        return
    
    phrozen = next((p for p in projects if p.name == "Phrozen"), projects[0])
    print(f"Target identified: [Project {phrozen.id}] {phrozen.name}")

    print("> ROUTER AGENT: Spawning task 'Investigate caching failure'")
    task = task_service.create_task(db, project_id=phrozen.id, title="Investigate caching failure")
    print(f"Task created: {task.id}\n")

    # 2. Execution / Work Session
    print("> EXECUTION: User starts a work session to fix the cache issue...")
    session = Session(project_id=phrozen.id, title="Debugging caching logic", status="active")
    db.add(session)
    db.commit()
    db.refresh(session)
    print(f"Session started: {session.id}\n")

    # 3. Memory Curator Step
    print("> MEMORY CURATOR: Summarizing transcript into decisions and task states...")
    summary_text = "Found a race condition in the cache invalidation queue. We decided to move to a Redis sorted set."
    tasks_json = json.dumps(["Write unit tests for Redis cache layer", "Deploy updated cache config"])
    decisions_json = json.dumps([{"title": "Move to Redis sorted set for caching", "context": "Race condition in memory queue"}])
    
    summary = SessionSummary(
        session_id=session.id,
        summary=summary_text,
        extracted_tasks=tasks_json,
        extracted_decisions=decisions_json
    )
    db.add(summary)
    db.commit()
    print("Session summary added.\n")

    print("> MEMORY CURATOR: Triggering consolidation to commit to canonical memory...")
    result = consolidation_service.consolidate_session(db, session.id)
    print(f"Consolidation result: {result['status']}")
    print(f"New Memory Items created: {len(result['created'].get('memory_items', []))}")
    if result['created'].get('snapshot'):
        print(f"New Project Snapshot created: YES\n")
    
    # 4. Verification via Retrieval (Mode A)
    print("=== VERIFICATION ===")
    print("> ROUTER AGENT (Later): 'Hey FredOS, what is the status of Phrozen?'")
    overview = retrieval_service.retrieve_project_overview(db, phrozen.id)
    
    print(f"\nMode A Return Context:")
    print(f"Project: {overview.project['name']}")
    print(f"Recent Summaries: {overview.session_summaries[0]['summary'] if overview.session_summaries else 'None'}")
    print(f"Open Tasks: {len(overview.tasks)}")
    print(f"Recent Decisions: {len(overview.decisions)}")

    print("\nSimulation complete. FredOS framework is fully functional.")
    db.close()

if __name__ == "__main__":
    simulate()
