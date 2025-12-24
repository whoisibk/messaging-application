"""add default uuid to tables

Revision ID: 5b5f8049cfeb
Revises: 14dd8020c6b3
Create Date: 2025-12-24 03:14:16.867466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b5f8049cfeb'
down_revision: Union[str, Sequence[str], None] = '14dd8020c6b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
