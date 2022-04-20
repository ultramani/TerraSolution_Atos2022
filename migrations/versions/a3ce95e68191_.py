"""empty message

Revision ID: a3ce95e68191
Revises: 4c2878236dff
Create Date: 2022-04-20 16:43:11.438850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ce95e68191'
down_revision = '4c2878236dff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_crops_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=True),
    sa.Column('crop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['crop_id'], ['tbl_crops.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['report_id'], ['tbl_reports.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('tbl_reports', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tbl_reports', 'tbl_users', ['user_id'], ['user_id'])
    op.add_column('tbl_users', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('tbl_users_reportid_fkey', 'tbl_users', type_='foreignkey')
    op.drop_column('tbl_users', 'reportid')
    op.drop_column('tbl_users', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_users', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('tbl_users', sa.Column('reportid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('tbl_users_reportid_fkey', 'tbl_users', 'tbl_reports', ['reportid'], ['id'])
    op.drop_column('tbl_users', 'user_id')
    op.drop_constraint(None, 'tbl_reports', type_='foreignkey')
    op.drop_column('tbl_reports', 'user_id')
    op.drop_table('tbl_crops_report')
    # ### end Alembic commands ###
