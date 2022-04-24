"""empty message

Revision ID: 4e17fb81e349
Revises: daf539a14734
Create Date: 2022-04-24 16:32:26.317555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4e17fb81e349'
down_revision = 'daf539a14734'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('location', sa.ARRAY(sa.Float()), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('bbox', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('sides', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('polygon', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('params', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('numberOfPlants', sa.Integer(), nullable=True),
    sa.Column('avgMonthlyTemperaturePlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('avgMonthlyPrecipitationPlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('avgMonthlyHumidityPlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('avgMonthlySoilmoisturePlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('avgMonthlySoiltemperaturePlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('avgMonthlyRadiationPlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('avgMonthlyWindVelocityPlants', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('plantsScores', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('plantsNames', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('plantsBadges', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('plantsLifePeriod', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('priceperkg', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('waterneeded', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('watercost', sa.ARRAY(sa.Float()), nullable=True),
    sa.Column('benefit', sa.ARRAY(sa.Float()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['tbl_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_reports')
    # ### end Alembic commands ###
