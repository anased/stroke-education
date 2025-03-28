"""empty message

Revision ID: d1682c1819b9
Revises: 
Create Date: 2025-02-13 19:44:27.407036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1682c1819b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('risk_factor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stroke_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('risk_factor_management',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('risk_factor_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['risk_factor_id'], ['risk_factor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stroke_management',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stroke_type_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['stroke_type_id'], ['stroke_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stroke_management')
    op.drop_table('risk_factor_management')
    op.drop_table('stroke_type')
    op.drop_table('risk_factor')
    # ### end Alembic commands ###
