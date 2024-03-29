"""empty message

Revision ID: 8c7b1c01734c
Revises: 1a68cf42cc99
Create Date: 2018-12-11 14:48:45.307458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c7b1c01734c'
down_revision = '1a68cf42cc99'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subjects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_es', sa.Unicode(length=2048), nullable=True))

    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subjects', schema=None) as batch_op:
        batch_op.drop_column('name_es')

    # ### end Alembic commands ###
