"""merge heads

Revision ID: e42a105954c8
Revises: 9f8c3e2d1a7b, a3c1f8e20d47
Create Date: 2026-04-05 15:44:05.156985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e42a105954c8'
down_revision: Union[str, Sequence[str], None] = ('9f8c3e2d1a7b', 'a3c1f8e20d47')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
