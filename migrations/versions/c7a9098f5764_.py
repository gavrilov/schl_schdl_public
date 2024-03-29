"""empty message

Revision ID: c7a9098f5764
Revises: 3a7516a4cc6a
Create Date: 2018-11-20 08:53:15.719825

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c7a9098f5764'
down_revision = '3a7516a4cc6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('color', sa.Unicode(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subjects', 'color')
    # ### end Alembic commands ###
