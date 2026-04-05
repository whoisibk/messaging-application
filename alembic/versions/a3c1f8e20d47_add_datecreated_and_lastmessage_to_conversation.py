"""add dateCreated and lastMessage to conversation

Revision ID: a3c1f8e20d47
Revises: 5b5f8049cfeb
Create Date: 2026-04-04 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a3c1f8e20d47"
down_revision: Union[str, Sequence[str], None] = "5b5f8049cfeb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("conversation", sa.Column("dateCreated", sa.DateTime(), nullable=True))
    op.add_column("conversation", sa.Column("lastMessage", sa.String(250), nullable=True))


def downgrade() -> None:
    op.drop_column("conversation", "lastMessage")
    op.drop_column("conversation", "dateCreated")
