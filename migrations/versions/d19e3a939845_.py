"""empty message

Revision ID: d19e3a939845
Revises: 4f667e1e5074
Create Date: 2022-04-16 23:08:11.643357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd19e3a939845'
down_revision = '4f667e1e5074'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tbl_reports', 'polygon')
    op.drop_column('tbl_reports', 'avgMonthlyHumidityPlants')
    op.drop_column('tbl_reports', 'avgMonthlySoiltemperature')
    op.drop_column('tbl_reports', 'avgMonthlySoiltemperaturePlants')
    op.drop_column('tbl_reports', 'windDirection')
    op.drop_column('tbl_reports', 'avgMonthlyWindDirection')
    op.drop_column('tbl_reports', 'plantsScore')
    op.drop_column('tbl_reports', 'avgMonthlyPrecipitationPlants')
    op.drop_column('tbl_reports', 'avgMonthlySoilmoisturePlants')
    op.drop_column('tbl_reports', 'name')
    op.drop_column('tbl_reports', 'areaSquareHectare')
    op.drop_column('tbl_reports', 'avgMonthlyTemperaturePlants')
    op.drop_column('tbl_reports', 'avgMonthlyTemperature')
    op.drop_column('tbl_reports', 'avgMonthlyRadiation')
    op.drop_column('tbl_reports', 'avgMonthlyHumidity')
    op.drop_column('tbl_reports', 'bbox')
    op.drop_column('tbl_reports', 'numberOfPlants')
    op.drop_column('tbl_reports', 'avgMonthlyRadiationPlants')
    op.drop_column('tbl_reports', 'avgMonthlySoilmoisture')
    op.drop_column('tbl_reports', 'avgMonthlyWindDirectionPlants')
    op.drop_column('tbl_reports', 'avgMonthlyPrecipitation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_reports', sa.Column('avgMonthlyPrecipitation', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyWindDirectionPlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoilmoisture', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyRadiationPlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('numberOfPlants', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('bbox', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyHumidity', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyRadiation', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyTemperature', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyTemperaturePlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('areaSquareHectare', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoilmoisturePlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyPrecipitationPlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('plantsScore', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyWindDirection', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('windDirection', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoiltemperaturePlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoiltemperature', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyHumidityPlants', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('polygon', postgresql.BYTEA(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###