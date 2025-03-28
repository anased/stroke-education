"""Add authentication fields to user model

Revision ID: fbb7e439e1d3
Revises: d1682c1819b9
Create Date: 2025-03-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbb7e439e1d3'
down_revision = 'd1682c1819b9'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to user table but keep email nullable
    with op.batch_alter_table('user') as batch_op:
        # We'll keep email nullable for existing users
        # but modify our form validation to require email for new users
        batch_op.add_column(sa.Column('password_hash', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('last_login', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_registered', sa.Boolean(), nullable=False, server_default='0'))


def downgrade():
    # Remove columns from user table
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('is_registered')
        batch_op.drop_column('last_login')
        batch_op.drop_column('password_hash')