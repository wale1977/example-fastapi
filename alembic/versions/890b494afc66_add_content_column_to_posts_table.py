"""add content column to posts table

Revision ID: 890b494afc66
Revises: 89626f0023b6
Create Date: 2024-01-03 19:52:31.148879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '890b494afc66'
down_revision: Union[str, None] = '89626f0023b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
