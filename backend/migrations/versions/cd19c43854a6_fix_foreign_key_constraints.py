"""Fix foreign key constraints

Revision ID: cd19c43854a6
Revises: 39c5b09c883a
Create Date: 2020-05-06 12:59:03.159668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd19c43854a6'
down_revision = '39c5b09c883a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('categories', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'categories', 'users', ['user_id'], ['id'])
    op.add_column('transactions', sa.Column('category_id', sa.String(length=50), nullable=True))
    op.drop_constraint('transactions_category_fkey', 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'categories', ['category_id'], ['id'])
    op.drop_column('transactions', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('category', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key('transactions_category_fkey', 'transactions', 'categories', ['category'], ['name'])
    op.drop_column('transactions', 'category_id')
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.drop_column('categories', 'user_id')
    op.drop_column('categories', 'id')
    # ### end Alembic commands ###