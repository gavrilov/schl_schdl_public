"""empty message

Revision ID: 01978868721f
Revises: 980194f8c5b1
Create Date: 2018-09-15 00:12:43.858189

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '01978868721f'
down_revision = '980194f8c5b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', table_name='users')
    op.alter_column('users', 'username', nullable=False, new_column_name='email')
    op.alter_column('users', 'password_hash', nullable=False, new_column_name='password')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.alter_column('users', 'email', nullable=False, new_column_name='username')
    op.alter_column('users', 'password', nullable=False, new_column_name='password_hash')
    op.create_index('ix_users_username', 'users', ['username'], unique=1)
    # ### end Alembic commands ###