"""Add primary_currency column

Revision ID: 435838aad13f
Revises: 30b68c301740
Create Date: 2020-05-24 19:55:53.636765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '435838aad13f'
down_revision = '30b68c301740'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('primary_currency', sa.String(length=3), nullable=True))
    op.add_column('users', sa.Column('selected_currency', sa.String(length=3), nullable=True))
    op.drop_column('users', 'default_currency')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('default_currency', sa.VARCHAR(length=3), autoincrement=False, nullable=True))
    op.drop_column('users', 'selected_currency')
    op.drop_column('users', 'primary_currency')
    # ### end Alembic commands ###