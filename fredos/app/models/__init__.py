"""FredOS models — import all ORM classes so Alembic/Base.metadata sees them."""

from app.models.project import Project, ProjectSnapshot
from app.models.task import Task, TaskDependency
from app.models.session import Session, SessionSummary
from app.models.memory import MemoryItem, MemoryLink
from app.models.research import ResearchNote, Decision
from app.models.document import Document
from app.models.inbox import InboxItem
from app.models.execution import ExecutionRun
from app.models.daily_brief import DailyBrief
from app.models.event_log import EventLog

__all__ = [
    "Project",
    "ProjectSnapshot",
    "Task",
    "TaskDependency",
    "Session",
    "SessionSummary",
    "MemoryItem",
    "MemoryLink",
    "ResearchNote",
    "Decision",
    "Document",
    "InboxItem",
    "ExecutionRun",
    "DailyBrief",
    "EventLog",
]
