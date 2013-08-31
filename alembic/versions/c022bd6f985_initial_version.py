"""Initial version

Revision ID: c022bd6f985
Revises: None
Create Date: 2013-08-31 01:55:42.446060

"""

# revision identifiers, used by Alembic.
revision = 'c022bd6f985'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monitor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=128), nullable=False),
    sa.Column('serial', sa.String(length=128), nullable=False),
    sa.Column('reserved_by', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('monitor')
    ### end Alembic commands ###