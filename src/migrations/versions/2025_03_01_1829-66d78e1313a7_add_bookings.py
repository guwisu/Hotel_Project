"""add bookings

Revision ID: 66d78e1313a7
Revises: b0a5a3343e15
Create Date: 2025-03-01 18:29:19.607439

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "66d78e1313a7"
down_revision: Union[str, None] = "b0a5a3343e15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("data_from", sa.Date(), nullable=False),
        sa.Column("data_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
