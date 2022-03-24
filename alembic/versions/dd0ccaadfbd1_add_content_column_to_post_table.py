"""add Content column to post table

Revision ID: dd0ccaadfbd1
Revises: 1b4c3ff647f1
Create Date: 2022-03-24 15:50:40.360858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd0ccaadfbd1'
down_revision = '1b4c3ff647f1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
