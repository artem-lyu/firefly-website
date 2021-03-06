"""empty message

Revision ID: 756480e30882
Revises: fff6d3295e9c
Create Date: 2021-08-08 16:06:40.874908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '756480e30882'
down_revision = 'fff6d3295e9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.drop_index('ix_notification_name')
        batch_op.drop_index('ix_notification_timestamp')

    op.drop_table('notification')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notification', schema=None) as batch_op:
        batch_op.create_index('ix_notification_timestamp', ['timestamp'], unique=False)
        batch_op.create_index('ix_notification_name', ['name'], unique=False)

    # ### end Alembic commands ###
