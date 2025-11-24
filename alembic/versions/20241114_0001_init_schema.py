"""Initial schema for core tables.

Revision ID: 20241114_0001
Revises:
Create Date: 2025-11-14 11:40:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20241114_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analysis_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("text_hash", sa.String(length=128), nullable=False),
        sa.Column("label", sa.String(length=32), nullable=False),
        sa.Column("empathy_score", sa.Float, nullable=False),
        sa.Column("crisis_probability", sa.Float, nullable=False),
        sa.Column("evidence", sa.JSON, nullable=False),
        sa.Column("model_version", sa.String(length=64), nullable=False),
        sa.Column("rule_version", sa.String(length=64)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_analysis_logs_request_id",
        "analysis_logs",
        ["request_id"],
    )
    op.create_index(
        "ix_analysis_logs_text_hash",
        "analysis_logs",
        ["text_hash"],
    )

    op.create_table(
        "filter_audits",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("text_hash", sa.String(length=128), nullable=False),
        sa.Column("decision", sa.String(length=16), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("allow", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("matched_rules", sa.JSON, nullable=False),
        sa.Column("analyzer_snapshot", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_filter_audits_request_id",
        "filter_audits",
        ["request_id"],
    )
    op.create_index(
        "ix_filter_audits_text_hash",
        "filter_audits",
        ["text_hash"],
    )

    op.create_table(
        "event_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("keyword", sa.String(length=128), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("emotion_series", sa.JSON, nullable=False),
        sa.Column("crisis_summary", sa.JSON, nullable=False),
        sa.Column("representative_quotes", sa.JSON, nullable=False),
        sa.Column("network_graph", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_event_snapshots_keyword",
        "event_snapshots",
        ["keyword"],
    )

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("room_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("text", sa.String(length=2048), nullable=False),
        sa.Column("sentiment", sa.String(length=32), nullable=False),
        sa.Column("crisis_probability", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_chat_messages_room_id",
        "chat_messages",
        ["room_id"],
    )
    op.create_index(
        "ix_chat_messages_user_id",
        "chat_messages",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_chat_messages_user_id", table_name="chat_messages")
    op.drop_index("ix_chat_messages_room_id", table_name="chat_messages")
    op.drop_table("chat_messages")

    op.drop_index("ix_event_snapshots_keyword", table_name="event_snapshots")
    op.drop_table("event_snapshots")

    op.drop_index("ix_filter_audits_text_hash", table_name="filter_audits")
    op.drop_index("ix_filter_audits_request_id", table_name="filter_audits")
    op.drop_table("filter_audits")

    op.drop_index("ix_analysis_logs_text_hash", table_name="analysis_logs")
    op.drop_index("ix_analysis_logs_request_id", table_name="analysis_logs")
    op.drop_table("analysis_logs")
