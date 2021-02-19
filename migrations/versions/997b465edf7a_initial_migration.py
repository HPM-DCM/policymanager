"""initial migration

Revision ID: 997b465edf7a
Revises: 
Create Date: 2020-10-21 20:12:34.871434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '997b465edf7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('errpolicy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.String(length=10), nullable=True),
    sa.Column('pcrf', sa.String(length=20), nullable=True),
    sa.Column('fact', sa.String(length=5), nullable=True),
    sa.Column('policy_id', sa.String(length=33), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('net_value', sa.String(length=500), nullable=True),
    sa.Column('stand_value', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mlepolicy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.sa.String(length=10), nullable=True),
    sa.Column('pcrf', sa.String(length=20), nullable=True),
    sa.Column('fact', sa.String(length=5), nullable=True),
    sa.Column('policy_id', sa.String(length=33), nullable=True),
    sa.Column('con_more', sa.String(length=500), nullable=True),
    sa.Column('con_less', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mspolicy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.sa.String(length=10), nullable=True),
    sa.Column('pcrf', sa.String(length=20), nullable=True),
    sa.Column('fact', sa.String(length=5), nullable=True),
    sa.Column('policy_id', sa.String(length=33), nullable=True),
    sa.Column('policy_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rbpolicy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.sa.String(length=10), nullable=True),
    sa.Column('pcrf', sa.String(length=20), nullable=True),
    sa.Column('fact', sa.String(length=5), nullable=True),
    sa.Column('policy_id', sa.String(length=50), nullable=True),
    sa.Column('policy_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stdlib',
    sa.Column('policy_id', sa.String(length=33), nullable=False),
    sa.Column('policy_name', sa.String(length=200), nullable=True),
    sa.Column('demand_city', sa.String(length=5), nullable=True),
    sa.Column('online_city', sa.String(length=20), nullable=True),
    sa.Column('policy_type', sa.String(length=10), nullable=True),
    sa.Column('policy_attribute', sa.String(length=10), nullable=True),
    sa.Column('bear_type', sa.String(length=5), nullable=True),
    sa.Column('policy_QCI', sa.Integer(), nullable=True),
    sa.Column('policy_ARP', sa.Integer(), nullable=True),
    sa.Column('policy_speed', sa.String(length=300), nullable=True),
    sa.Column('policy_other', sa.String(length=300), nullable=True),
    sa.Column('time_online', sa.DateTime(), nullable=True),
    sa.Column('time_offline', sa.DateTime(), nullable=True),
    sa.Column('policy_status', sa.String(length=5), nullable=True),
    sa.Column('fact', sa.String(length=15), nullable=True),
    sa.Column('SMS_content', sa.String(length=500), nullable=True),
    sa.Column('priority_zx', sa.String(length=10), nullable=True),
    sa.Column('priority_hw', sa.String(length=10), nullable=True),
    sa.Column('priority_eri', sa.String(length=10), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('policy_id')
    )
    op.create_table('stdlib_scriap',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('policy_id', sa.String(length=33), nullable=True),
    sa.Column('fact', sa.String(length=5), nullable=True),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stdlib_scriap')
    op.drop_table('stdlib')
    op.drop_table('rbpolicy')
    op.drop_table('mspolicy')
    op.drop_table('mlepolicy')
    op.drop_table('errpolicy')
    # ### end Alembic commands ###
