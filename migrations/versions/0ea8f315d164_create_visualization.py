"""create_visualization

Revision ID: 0ea8f315d164
Revises: 44dfe4213d01
Create Date: 2023-02-19 10:57:30.962543

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0ea8f315d164'
down_revision = '44dfe4213d01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visualization',
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_index(op.f('ix_visualization_name'), 'visualization', ['name'], unique=False)
    op.create_index(op.f('ix_visualization_type'), 'visualization', ['type'], unique=False)
    op.create_index(op.f('ix_visualization_uid'), 'visualization', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_visualization_uid'), table_name='visualization')
    op.drop_index(op.f('ix_visualization_type'), table_name='visualization')
    op.drop_index(op.f('ix_visualization_name'), table_name='visualization')
    op.drop_table('visualization')
    # ### end Alembic commands ###