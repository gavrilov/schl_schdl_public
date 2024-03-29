"""empty message

Revision ID: f01a2ef5a0a8
Revises: 559111379c8c
Create Date: 2019-02-19 13:11:51.148601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f01a2ef5a0a8'
down_revision = '559111379c8c'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('read_only', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.drop_column('read_only')

    # ### end Alembic commands ###
