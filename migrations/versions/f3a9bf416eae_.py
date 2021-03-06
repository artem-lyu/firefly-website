"""empty message

Revision ID: f3a9bf416eae
Revises: db0b5956107d
Create Date: 2021-07-27 14:01:03.401831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a9bf416eae'
down_revision = 'db0b5956107d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('contact_phone', sa.Integer(), nullable=True),
    sa.Column('official_id', sa.Integer(), nullable=True),
    sa.Column('last_seen', sa.String(length=140), nullable=True),
    sa.Column('about_me', sa.DateTime(), nullable=True),
    sa.Column('number_jobs', sa.Integer(), nullable=True),
    sa.Column('home_address', sa.String(length=120), nullable=True),
    sa.Column('date_birth', sa.String(length=10), nullable=True),
    sa.Column('location', sa.String(length=20), nullable=True),
    sa.Column('legal_person_name', sa.String(length=10), nullable=True),
    sa.Column('legal_person_phone', sa.Integer(), nullable=True),
    sa.Column('physical_address', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_contact_phone'), ['contact_phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_home_address'), ['home_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_legal_person_name'), ['legal_person_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_legal_person_phone'), ['legal_person_phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_location'), ['location'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_number_jobs'), ['number_jobs'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_official_id'), ['official_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_physical_address'), ['physical_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('job_posting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position_title', sa.String(length=30), nullable=True),
    sa.Column('location', sa.String(length=30), nullable=True),
    sa.Column('contact_phone', sa.Integer(), nullable=True),
    sa.Column('physical_address', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job_posting', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_posting_contact_phone'), ['contact_phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_posting_location'), ['location'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_posting_physical_address'), ['physical_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_posting_position_title'), ['position_title'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_posting_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_index('ix_employees_contact_phone')
        batch_op.drop_index('ix_employees_email')
        batch_op.drop_index('ix_employees_home_address')
        batch_op.drop_index('ix_employees_location')
        batch_op.drop_index('ix_employees_number_jobs')
        batch_op.drop_index('ix_employees_username')

    op.drop_table('employees')
    with op.batch_alter_table('employers', schema=None) as batch_op:
        batch_op.drop_index('ix_employers_contact_phone')
        batch_op.drop_index('ix_employers_email')
        batch_op.drop_index('ix_employers_legal_person_name')
        batch_op.drop_index('ix_employers_legal_person_phone')
        batch_op.drop_index('ix_employers_physical_address')
        batch_op.drop_index('ix_employers_username')

    op.drop_table('employers')
    with op.batch_alter_table('job-postings', schema=None) as batch_op:
        batch_op.drop_index('ix_job-postings_contact_phone')
        batch_op.drop_index('ix_job-postings_date_posted')
        batch_op.drop_index('ix_job-postings_location')
        batch_op.drop_index('ix_job-postings_physical_address')
        batch_op.drop_index('ix_job-postings_position_title')

    op.drop_table('job-postings')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job-postings',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('position_title', sa.VARCHAR(length=30), nullable=True),
    sa.Column('location', sa.VARCHAR(length=30), nullable=True),
    sa.Column('contact_phone', sa.INTEGER(), nullable=True),
    sa.Column('physical_address', sa.VARCHAR(length=100), nullable=True),
    sa.Column('date_posted', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job-postings', schema=None) as batch_op:
        batch_op.create_index('ix_job-postings_position_title', ['position_title'], unique=False)
        batch_op.create_index('ix_job-postings_physical_address', ['physical_address'], unique=False)
        batch_op.create_index('ix_job-postings_location', ['location'], unique=False)
        batch_op.create_index('ix_job-postings_date_posted', ['date_posted'], unique=False)
        batch_op.create_index('ix_job-postings_contact_phone', ['contact_phone'], unique=False)

    op.create_table('employers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('legal_person_name', sa.VARCHAR(length=10), nullable=True),
    sa.Column('legal_person_phone', sa.INTEGER(), nullable=True),
    sa.Column('contact_phone', sa.INTEGER(), nullable=True),
    sa.Column('physical_address', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('employers', schema=None) as batch_op:
        batch_op.create_index('ix_employers_username', ['username'], unique=False)
        batch_op.create_index('ix_employers_physical_address', ['physical_address'], unique=False)
        batch_op.create_index('ix_employers_legal_person_phone', ['legal_person_phone'], unique=False)
        batch_op.create_index('ix_employers_legal_person_name', ['legal_person_name'], unique=False)
        batch_op.create_index('ix_employers_email', ['email'], unique=False)
        batch_op.create_index('ix_employers_contact_phone', ['contact_phone'], unique=False)

    op.create_table('employees',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('number_jobs', sa.INTEGER(), nullable=True),
    sa.Column('home_address', sa.VARCHAR(length=120), nullable=True),
    sa.Column('contact_phone', sa.INTEGER(), nullable=True),
    sa.Column('date_birth', sa.VARCHAR(length=10), nullable=True),
    sa.Column('location', sa.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.create_index('ix_employees_username', ['username'], unique=False)
        batch_op.create_index('ix_employees_number_jobs', ['number_jobs'], unique=False)
        batch_op.create_index('ix_employees_location', ['location'], unique=False)
        batch_op.create_index('ix_employees_home_address', ['home_address'], unique=False)
        batch_op.create_index('ix_employees_email', ['email'], unique=False)
        batch_op.create_index('ix_employees_contact_phone', ['contact_phone'], unique=False)

    with op.batch_alter_table('job_posting', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_posting_timestamp'))
        batch_op.drop_index(batch_op.f('ix_job_posting_position_title'))
        batch_op.drop_index(batch_op.f('ix_job_posting_physical_address'))
        batch_op.drop_index(batch_op.f('ix_job_posting_location'))
        batch_op.drop_index(batch_op.f('ix_job_posting_contact_phone'))

    op.drop_table('job_posting')
    op.drop_table('followers')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_physical_address'))
        batch_op.drop_index(batch_op.f('ix_user_official_id'))
        batch_op.drop_index(batch_op.f('ix_user_number_jobs'))
        batch_op.drop_index(batch_op.f('ix_user_location'))
        batch_op.drop_index(batch_op.f('ix_user_legal_person_phone'))
        batch_op.drop_index(batch_op.f('ix_user_legal_person_name'))
        batch_op.drop_index(batch_op.f('ix_user_home_address'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_contact_phone'))

    op.drop_table('user')
    # ### end Alembic commands ###
