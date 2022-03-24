"""update post table

Revision ID: ea004bfbbba7
Revises: e6a58105713e
Create Date: 2022-03-24 16:53:32.678400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea004bfbbba7'
down_revision = 'e6a58105713e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published', sa.Boolean(),nullable=False,server_default='FALSE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
    server_default= sa.text('now()'), nullable=False),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
