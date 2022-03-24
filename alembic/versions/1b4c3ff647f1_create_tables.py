"""Create tables

Revision ID: 1b4c3ff647f1
Revises: 
Create Date: 2022-03-24 15:24:41.784032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b4c3ff647f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
    sa.Column('title', sa.String(), nullable=False) )
    pass


def downgrade():
    op.drop_table('posts')
    pass
