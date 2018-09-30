"""empty message

Revision ID: 8f8259edae3c
Revises: 7f24b274fb93
Create Date: 2018-09-30 00:41:55.704290

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8f8259edae3c'
down_revision = '7f24b274fb93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stripe_id', sa.Unicode(length=2048), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('stripe_id')

    # ### end Alembic commands ###
