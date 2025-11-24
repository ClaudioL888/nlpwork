"""Add text column to analysis_logs

Revision ID: 20241114_0002
Revises: 20241114_0001
Create Date: 2025-11-14 14:05:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20241114_0002"
down_revision: Union[str, None] = "20241114_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("analysis_logs", sa.Column("text", sa.String(length=2048), nullable=False, server_default=""))
    op.alter_column("analysis_logs", "text", server_default=None)


def downgrade() -> None:
    op.drop_column("analysis_logs", "text")
