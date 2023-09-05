"""db_creation

Revision ID: 2ceb57b0a4f0
Revises: ff4620c9a63f
Create Date: 2023-09-05 20:09:37.166341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ceb57b0a4f0'
down_revision: Union[str, None] = 'ff4620c9a63f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
