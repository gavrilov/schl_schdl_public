"""empty message

Revision ID: 980194f8c5b1
Revises: 557cc6db23f5
Create Date: 2018-09-14 22:37:03.512284

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '980194f8c5b1'
down_revision = '557cc6db23f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed_at')
    op.drop_column('users', 'active')
    # ### end Alembic commands ###