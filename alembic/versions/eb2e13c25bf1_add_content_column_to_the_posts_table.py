"""Add content column to the posts table

Revision ID: eb2e13c25bf1
Revises: 4df681025dee
Create Date: 2025-04-02 12:31:56.758900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb2e13c25bf1'
down_revision: Union[str, None] = '4df681025dee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
