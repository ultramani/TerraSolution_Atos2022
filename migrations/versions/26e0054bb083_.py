"""empty message

Revision ID: 26e0054bb083
Revises: 88e1cdfe7100
Create Date: 2022-04-17 22:56:44.551169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '26e0054bb083'
down_revision = '88e1cdfe7100'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_crops', sa.Column('waterPerArea', sa.Integer(), nullable=True))
    op.add_column('tbl_reports', sa.Column('area', sa.Float(), nullable=True))
    op.alter_column('tbl_reports', 'location',
               existing_type=postgresql.ARRAY(sa.INTEGER()),
               nullable=False)
    op.alter_column('tbl_reports', 'name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_column('tbl_reports', 'areaSquareHectare')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_reports', sa.Column('areaSquareHectare', sa.INTEGER(), autoincrement=False, nullable=True))
    op.alter_column('tbl_reports', 'name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('tbl_reports', 'location',
               existing_type=postgresql.ARRAY(sa.INTEGER()),
               nullable=True)
    op.drop_column('tbl_reports', 'area')
    op.drop_column('tbl_crops', 'waterPerArea')
    # ### end Alembic commands ###
