"""empty message

Revision ID: 49c6fb72ad95
Revises: a1af6b9cd67f
Create Date: 2019-07-02 16:56:10.740151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49c6fb72ad95'
down_revision = 'a1af6b9cd67f'
branch_labels = None
depends_on = None


def upgrade():
# ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enrollments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp_last_change', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
# ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enrollments', schema=None) as batch_op:
        batch_op.drop_column('timestamp_last_change')

    # ### end Alembic commands ###
