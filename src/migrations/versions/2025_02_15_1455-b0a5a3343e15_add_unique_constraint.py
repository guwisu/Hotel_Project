"""add unique constraint

Revision ID: b0a5a3343e15
Revises: 5635c26a90e4
Create Date: 2025-02-15 14:55:53.753883

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b0a5a3343e15"
down_revision: Union[str, None] = "5635c26a90e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
