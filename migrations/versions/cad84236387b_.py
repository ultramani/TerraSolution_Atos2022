"""empty message

Revision ID: cad84236387b
Revises: 40d065b5dd14
Create Date: 2022-04-07 15:09:33.933887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cad84236387b'
down_revision = '40d065b5dd14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('location', sa.ARRAY(sa.Integer(), dimensions=5), nullable=False),
    sa.Column('avgMonthlytemperature', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgMonthlyprecipitation', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgMonthlyhumidity', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgMonthlysoilmoisture', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgMonthlyradiation', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgAnnualtemperature', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgAnnualprecipitation', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgAnnualhumidity', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgAnnualsoilmoisture', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.Column('avgAnnualradiation', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_reports')
    # ### end Alembic commands ###
