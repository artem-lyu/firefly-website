"""is_employer boolean property added

Revision ID: 15c9715cfd02
Revises: 7fb4c3c40adb
Create Date: 2021-08-17 16:38:43.292746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15c9715cfd02'
down_revision = '7fb4c3c40adb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_employer', sa.Boolean(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_is_employer'), ['is_employer'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_is_employer'))
        batch_op.drop_column('is_employer')

    # ### end Alembic commands ###
