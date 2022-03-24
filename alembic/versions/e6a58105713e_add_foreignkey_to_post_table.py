"""add foreignkey to post table

Revision ID: e6a58105713e
Revises: a97ac78441bf
Create Date: 2022-03-24 16:45:45.777156

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6a58105713e'
down_revision = 'a97ac78441bf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], 
    remote_cols=['id'], ondelete= 'CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
