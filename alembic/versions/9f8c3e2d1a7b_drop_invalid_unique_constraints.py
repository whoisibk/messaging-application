"""drop invalid unique constraints

Revision ID: 9f8c3e2d1a7b
Revises: 5b5f8049cfeb
Create Date: 2026-03-30 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9f8c3e2d1a7b"
down_revision: Union[str, Sequence[str], None] = "5b5f8049cfeb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("message_recipientId_key", "message", type_="unique")
    op.drop_constraint("conversation_user1_Id_key", "conversation", type_="unique")
    op.drop_constraint("conversation_user2_Id_key", "conversation", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        "message_recipientId_key", "message", ["recipientId"]
    )
    op.create_unique_constraint(
        "conversation_user1_Id_key", "conversation", ["user1_Id"]
    )
    op.create_unique_constraint(
        "conversation_user2_Id_key", "conversation", ["user2_Id"]
    )
