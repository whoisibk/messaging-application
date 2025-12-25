"""add default uuid to tables

Revision ID: 5b5f8049cfeb
Revises: 14dd8020c6b3
Create Date: 2025-12-24 03:14:16.867466

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision: str = "5b5f8049cfeb"
down_revision: Union[str, Sequence[str], None] = "14dd8020c6b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # user table
    op.alter_column(
        table_name="user",
        column_name="userId",
        existing_type=sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )
    # message table
    op.alter_column(
        table_name="message",
        column_name="messageId",
        existing_type=sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )
    # conversation table
    op.alter_column(
        table_name="conversation",
        column_name="conversationId",
        existing_type=sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        table_name="user",
        column_name="userId",
        existing_type=sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
        server_default=None,
    )
    # message table
    op.alter_column(
        table_name="message",
        column_name="messageId",
        existing_type=sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
        server_default=None,
    )
    # conversation table
    op.alter_column(
        table_name="conversation",
        column_name="conversationId",
        existing_type=sqlalchemy.dialects.postgresql.UUID(as_uuid=True),
        nullable=False,
        server_default=None,
    )
