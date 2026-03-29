"""Add OpenClaw session id and bridge indexes

Revision ID: b7f3b9d4a1c2
Revises: 639c35ae3d73
Create Date: 2026-03-29 04:35:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7f3b9d4a1c2"
down_revision: Union[str, None] = "639c35ae3d73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_names(bind) -> set[str]:
    inspector = sa.inspect(bind)
    return {col["name"] for col in inspector.get_columns("sessions")}


def _index_names(bind) -> set[str]:
    inspector = sa.inspect(bind)
    return {idx["name"] for idx in inspector.get_indexes("sessions")}


def upgrade() -> None:
    bind = op.get_bind()
    columns = _column_names(bind)
    indexes = _index_names(bind)

    with op.batch_alter_table("sessions") as batch_op:
        if "openclaw_session_id" not in columns:
            batch_op.add_column(sa.Column("openclaw_session_id", sa.String(length=200), nullable=True))

    if "ix_sessions_openclaw_session_id" not in indexes:
        op.create_index(
            "ix_sessions_openclaw_session_id",
            "sessions",
            ["openclaw_session_id"],
            unique=True,
        )

    if "ix_sessions_openclaw_session_key" not in indexes:
        op.create_index(
            "ix_sessions_openclaw_session_key",
            "sessions",
            ["openclaw_session_key"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    columns = _column_names(bind)
    indexes = _index_names(bind)

    if "ix_sessions_openclaw_session_key" in indexes:
        op.drop_index("ix_sessions_openclaw_session_key", table_name="sessions")

    if "ix_sessions_openclaw_session_id" in indexes:
        op.drop_index("ix_sessions_openclaw_session_id", table_name="sessions")

    if "openclaw_session_id" in columns:
        with op.batch_alter_table("sessions") as batch_op:
            batch_op.drop_column("openclaw_session_id")
