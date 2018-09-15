"""empty message

Revision ID: 43224d9b6c62
Revises: 9d7cc316f148
Create Date: 2018-09-15 02:39:08.925320

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '43224d9b6c62'
down_revision = '9d7cc316f148'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
                              existing_type=sa.VARCHAR(length=128),
                              type_=sa.Unicode(length=2048),
                              existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
                              existing_type=sa.Unicode(length=2048),
                              type_=sa.VARCHAR(length=128),
                              existing_nullable=True)

    # ### end Alembic commands ###
