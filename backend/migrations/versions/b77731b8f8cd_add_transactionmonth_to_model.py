"""Add TransactionMonth to model

Revision ID: b77731b8f8cd
Revises: 7bef7921341b
Create Date: 2019-10-23 16:13:51.527669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b77731b8f8cd'
down_revision = '7bef7921341b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction_months',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('transactions', sa.Column('transaction_month_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'transactions', 'transaction_months', ['transaction_month_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'transaction_month_id')
    op.drop_table('transaction_months')
    # ### end Alembic commands ###