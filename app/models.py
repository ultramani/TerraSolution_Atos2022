from enum import unique
from math import fabs

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager

from .databaseManager import db


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model,UserMixin):
    __tablename__='tbl_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # #Lista de roles del usuario, por si deseamos tener roles premium o admins
    # roles = db.relationship('Role', secondary='user_roles')
    reportid = db.Column(db.Integer, db.ForeignKey('tbl_reports.id'))

    #Función que indica a python como imprimir los objetos de esta clase
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class Role(db.Model):
#     __tablename__ = 'tbl_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=True)

# class UserRoles(db.Model):
#     __tablename__ = 'tbl_user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('tbl_users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('tbl_roles.id', ondelete='CASCADE'))

class report(db.Model):
    __tablename__ = 'tbl_reports'
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(128),nullable=False)
    date  = db.Column(db.Date(), nullable=False)
    location  = db.Column(db.ARRAY(db.Integer, dimensions=2))
    bbox  = db.Column(db.ARRAY(db.Integer, dimensions=4))
    polygon = db.Column(db.LargeBinary)
    areaSquareHectare = db.Column(db.Integer())
    

    #Asociacion a las plantas a las que les hemos dado el ok
    crops = db.relationship('crop', secondary='tbl_crops_report')
    #Datos obtenidos
        #Monthly data, en cada posición para cada planta aceptada
    avgMonthlyTemperature = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyPrecipitation = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyHumidity = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlySoilmoisture = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlySoiltemperature= db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyRadiation = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyWindDirection = db.Column(db.ARRAY(db.Integer, dimensions=12))
    windDirection =  db.Column(db.String(128),nullable=True)
    #Datos del analisis
        #Numero de palntas a las que le hemso dado el ok
    numberOfPlants = db.Column(db.Integer())
        #Media de los datos de los x meses por planta, en la posición cero se enccuentra el id del parametro
    avgMonthlyTemperaturePlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyPrecipitationPlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyHumidityPlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlySoilmoisturePlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlySoiltemperaturePlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyRadiationPlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
    avgMonthlyWindDirectionPlants = db.Column(db.ARRAY(db.Integer, dimensions=12))
        #Puntuaciones de plantas
    plantsScore = db.Column(db.ARRAY(db.Integer, dimensions=12))
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

class parameters(db.Model):
    __tablename__ = 'tbl_parameters'
    id = db.Column(db.Integer(), primary_key=True)

    shortname = db.Column(db.String(32))
    comunity = db.Column(db.String(3))
    longname = db.Column(db.String(64))
    unit = db.Column(db.String(16))

    def longnames():
        raw_params = db.session.query(parameters.longname).all()
        params = [value for value, in raw_params]
        return params
    
    def shortnames():
        raw_params = db.session.query(parameters.shortname).all()
        params = [value for value, in raw_params]
        return params
        
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()



class crop(db.Model):
    __tablename__ = 'tbl_crops'
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(128),nullable=False)
    reports = db.relationship("report", secondary="tbl_crops_report")
    #Nuemro de plantas plantables por hectarea.
    densityOfPopulation = db.Column(db.Integer())
    #Add a custom domain [tree, bush , grass]
    cropType = db.Column(db.String(128),nullable=False)
    #First array element will be the min value and the second one the max value and the third optimal value
    temperatureRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    humidityRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    soilmoistureRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    soiltemperatureRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    precipitationRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    radiationRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    windvelocityRange = db.Column(db.ARRAY(db.Integer, dimensions=3)) 
    #Money related section
    pricePerKg = db.Column(db.Integer())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()


class cropReport(db.Model):
    __tablename__ = 'tbl_crops_report'
    id = db.Column(db.Integer(), primary_key=True)
    report_id = db.Column(db.Integer(), db.ForeignKey('tbl_reports.id', ondelete='CASCADE'))
    crop_id = db.Column(db.Integer(), db.ForeignKey('tbl_crops.id', ondelete='CASCADE'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()