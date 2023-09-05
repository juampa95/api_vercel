"""db_creation

Revision ID: 6b0e01e8cde9
Revises: d659477893b5
Create Date: 2023-09-05 20:05:41.052756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b0e01e8cde9'
down_revision: Union[str, None] = 'd659477893b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
