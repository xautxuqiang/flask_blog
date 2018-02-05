"""empty message

Revision ID: 7980c17ee30c
Revises: 896814cd007c
Create Date: 2018-01-21 21:34:01.999807

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7980c17ee30c'
down_revision = '896814cd007c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('category', 'category_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_index(op.f('ix_category_category_name'), 'category', ['category_name'], unique=True)
    op.alter_column('post', 'title',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=True)
    op.alter_column('tag', 'tag_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.create_index(op.f('ix_tag_tag_name'), 'tag', ['tag_name'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_tag_tag_name'), table_name='tag')
    op.alter_column('tag', 'tag_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.alter_column('post', 'title',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.drop_index(op.f('ix_category_category_name'), table_name='category')
    op.alter_column('category', 'category_name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###