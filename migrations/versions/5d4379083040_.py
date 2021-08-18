"""empty message

Revision ID: 5d4379083040
Revises: b167603e366a
Create Date: 2021-08-08 15:48:06.698448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d4379083040'
down_revision = 'b167603e366a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('sender_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sender_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['sender_id'], ['id'])

    # ### end Alembic commands ###