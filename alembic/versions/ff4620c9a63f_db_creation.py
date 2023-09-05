"""db_creation

Revision ID: ff4620c9a63f
Revises: 6b0e01e8cde9
Create Date: 2023-09-05 20:07:48.939010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff4620c9a63f'
down_revision: Union[str, None] = '6b0e01e8cde9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
