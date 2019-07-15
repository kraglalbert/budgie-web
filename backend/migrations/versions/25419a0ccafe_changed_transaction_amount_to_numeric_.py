"""Changed Transaction amount to Numeric type

Revision ID: 25419a0ccafe
Revises: 644ed7fcad19
Create Date: 2019-07-14 21:54:51.263846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25419a0ccafe'
down_revision = '644ed7fcad19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', table_name='users')
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    # ### end Alembic commands ###
