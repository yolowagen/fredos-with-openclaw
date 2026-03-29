"""Continuous Autonomous Execution Loop — Phase 8.

This orchestrates the background runtime:
1. Checks the queue for pending tasks
2. Uses the router to determine the target agent
3. Simulates the agent execution
4. Captures outputs to the canonical memory system
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal, engine, Base
from app.services import queue_service, task_service, event_service
from app.agents import router_agent

def main_loop():
    print("=== FREDOS AUTONOMOUS LOOP INITIALIZED ===\n")
    
    # Ensure tables exist
    import app.models  # noqa
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        while True:
            # 1. Check for tasks
            task = queue_service.pick_next_task(db, actor="agent_loop_daemon")
            
            if not task:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(2)
                continue
                
            print(f"\n[LOOP] Picked Task #{task.id}: {task.title}")
            
            # 2. Route task
            target_agent = router_agent.route_task(task)
            print(f"[LOOP] Routing '{task.task_type}' task to => {target_agent}")
            
            event_service.emit_event(db, "task_routed", "agent_loop", {"task": task.id, "agent": target_agent})
            
            # 3. Simulate Execution
            print(f"[{target_agent.upper()}] Thinking...")
            time.sleep(1)
            print(f"[{target_agent.upper()}] Reading from canonical memory retrieval...")
            time.sleep(1)
            print(f"[{target_agent.upper()}] Completed simulated work.")
            
            # 4. Resolve task
            task_service.update_task(db, task.id, status="completed", description=f"{task.description}\n\n[Agent_Loop] Finished by {target_agent}")
            event_service.emit_event(db, "task_completed", target_agent, {"task_id": task.id})
            
            print(f"[LOOP] Task #{task.id} resolved. Continuing to next...\n")
            
    except KeyboardInterrupt:
        print("\n=== FREDOS LOOP HALTED ===")
    finally:
        db.close()

if __name__ == "__main__":
    main_loop()
