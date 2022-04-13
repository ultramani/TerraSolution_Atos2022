"""empty message

Revision ID: 8dbfa79bda36
Revises: df28f0094414
Create Date: 2022-04-13 19:24:54.811354

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8dbfa79bda36'
down_revision = 'df28f0094414'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_crops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('densityOfPopulation', sa.Integer(), nullable=True),
    sa.Column('cropType', sa.String(length=128), nullable=False),
    sa.Column('temperatureRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('humidityRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('soilmoistureRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('soiltemperatureRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('precipitationRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('radiationRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('windvelocityRange', sa.ARRAY(sa.Integer(), dimensions=3), nullable=True),
    sa.Column('pricePerKg', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbl_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shortname', sa.String(length=32), nullable=True),
    sa.Column('comunity', sa.String(length=3), nullable=True),
    sa.Column('longname', sa.String(length=64), nullable=True),
    sa.Column('unit', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tbl_crops_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=True),
    sa.Column('crop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['crop_id'], ['tbl_crops.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['report_id'], ['tbl_reports.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('tbl_reports', sa.Column('polygonLocation', sa.ARRAY(sa.BINARY(), dimensions=100), nullable=False))
    op.add_column('tbl_reports', sa.Column('areaSquareHectare', sa.Integer(), nullable=True))
    op.add_column('tbl_reports', sa.Column('windDirection', sa.String(length=128), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyTemperature', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyPrecipitation', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyHumidity', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoilmoisture', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoiltemperature', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyRadiation', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyWindDirection', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('numberOfPlants', sa.Integer(), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyTemperaturePlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyPrecipitationPlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyHumidityPlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoilmoisturePlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlySoiltemperaturePlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyRadiationPlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyWindDirectionPlants', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.add_column('tbl_reports', sa.Column('plantsScore', sa.ARRAY(sa.Integer(), dimensions=12), nullable=True))
    op.drop_column('tbl_reports', 'avgMonthlyradiation')
    op.drop_column('tbl_reports', 'avgAnnualradiation')
    op.drop_column('tbl_reports', 'avgAnnualtemperature')
    op.drop_column('tbl_reports', 'avgAnnualsoilmoisture')
    op.drop_column('tbl_reports', 'avgMonthlysoilmoisture')
    op.drop_column('tbl_reports', 'avgAnnualprecipitation')
    op.drop_column('tbl_reports', 'avgMonthlytemperature')
    op.drop_column('tbl_reports', 'avgMonthlyprecipitation')
    op.drop_column('tbl_reports', 'avgAnnualhumidity')
    op.drop_column('tbl_reports', 'avgMonthlyhumidity')
    op.add_column('tbl_users', sa.Column('reportid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tbl_users', 'tbl_reports', ['reportid'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tbl_users', type_='foreignkey')
    op.drop_column('tbl_users', 'reportid')
    op.add_column('tbl_reports', sa.Column('avgMonthlyhumidity', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgAnnualhumidity', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyprecipitation', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlytemperature', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgAnnualprecipitation', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlysoilmoisture', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgAnnualsoilmoisture', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgAnnualtemperature', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgAnnualradiation', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('tbl_reports', sa.Column('avgMonthlyradiation', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.drop_column('tbl_reports', 'plantsScore')
    op.drop_column('tbl_reports', 'avgMonthlyWindDirectionPlants')
    op.drop_column('tbl_reports', 'avgMonthlyRadiationPlants')
    op.drop_column('tbl_reports', 'avgMonthlySoiltemperaturePlants')
    op.drop_column('tbl_reports', 'avgMonthlySoilmoisturePlants')
    op.drop_column('tbl_reports', 'avgMonthlyHumidityPlants')
    op.drop_column('tbl_reports', 'avgMonthlyPrecipitationPlants')
    op.drop_column('tbl_reports', 'avgMonthlyTemperaturePlants')
    op.drop_column('tbl_reports', 'numberOfPlants')
    op.drop_column('tbl_reports', 'avgMonthlyWindDirection')
    op.drop_column('tbl_reports', 'avgMonthlyRadiation')
    op.drop_column('tbl_reports', 'avgMonthlySoiltemperature')
    op.drop_column('tbl_reports', 'avgMonthlySoilmoisture')
    op.drop_column('tbl_reports', 'avgMonthlyHumidity')
    op.drop_column('tbl_reports', 'avgMonthlyPrecipitation')
    op.drop_column('tbl_reports', 'avgMonthlyTemperature')
    op.drop_column('tbl_reports', 'windDirection')
    op.drop_column('tbl_reports', 'areaSquareHectare')
    op.drop_column('tbl_reports', 'polygonLocation')
    op.drop_table('tbl_crops_report')
    op.drop_table('tbl_parameters')
    op.drop_table('tbl_crops')
    # ### end Alembic commands ###
