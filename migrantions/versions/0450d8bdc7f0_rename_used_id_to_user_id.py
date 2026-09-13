"""rename used_id to user_id

Revision ID: 0450d8bdc7f0
Revises: 4a5a94e91045
Create Date: 2026-09-13 14:47:06.763737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0450d8bdc7f0'
down_revision: Union[str, Sequence[str], None] = '4a5a94e91045'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("moodle_connections", "used_id", new_column_name="user_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("moodle_connections", "user_id", new_column_name="used_id")
    pass
