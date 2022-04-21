from enum import unique
from math import fabs

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager

from .databaseManager import db
import datetime
from sqlalchemy.dialects.postgresql import JSON


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except:
        return None


class User(db.Model,UserMixin):
    __tablename__='tbl_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # #Lista de roles del usuario, por si deseamos tener roles premium o admins
    # roles = db.relationship('Role', secondary='user_roles')
    reports =  db.relationship("report", backref="user", lazy='dynamic')

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
        
    def getAllReports(self):
        return db.session.query(report).filter_by(id=self.id).all()

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

    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    location  = db.Column(db.ARRAY(db.Float),nullable=False)
    name = db.Column(db.String(128))
    bbox  = db.Column(db.ARRAY(db.Float))
    sides  = db.Column(db.ARRAY(db.Float))
    polygon = db.Column(db.ARRAY(db.Float))
    area = db.Column(db.Float)
   
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_users.id'))
    userx = db.relationship('User')

    #Asociacion a las plantas a las que les hemos dado el ok
    crops = db.relationship('crop', secondary='tbl_crops_report')
    #Datos obtenidos
    params = db.Column(JSON)
    #Datos del analisis
        #Numero de palntas a las que le hemso dado el ok
    numberOfPlants = db.Column(db.Integer())
        #Media de los datos de los x meses por planta, en la posición cero se enccuentra el id del parametro
    avgMonthlyTemperaturePlants = db.Column(db.ARRAY(db.Integer))
    avgMonthlyPrecipitationPlants = db.Column(db.ARRAY(db.Integer))
    avgMonthlyHumidityPlants = db.Column(db.ARRAY(db.Integer))
    avgMonthlySoilmoisturePlants = db.Column(db.ARRAY(db.Integer))
    avgMonthlySoiltemperaturePlants = db.Column(db.ARRAY(db.Integer))
    avgMonthlyRadiationPlants = db.Column(db.ARRAY(db.Integer))
    avgMonthlyWindDirectionPlants = db.Column(db.ARRAY(db.Integer))
        #Puntuaciones de plantas
    plantsScore = db.Column(db.ARRAY(db.Integer))
    
    def __init__ (self, location,user):
        self.location = location
        self.userx = user

    def getJson(self):
        json = {
            'date':self.date.strftime('%Y-%m-%d %H:%M:%S:%f'),
            'location': self.location[0],
            'name': self.name,
            'bbox': self.bbox[0],
            'sides': self.sides[0],
            'polygon': self.polygon[0],
            'area' : self.area,
            'params' : self.params
            }
        return json
    
    def getAllJson():
        reports = report.query.all()
        all = {'reports': []}
        for e in reports:
            all['reports'].append(e.getJson())
        return all
    
    def selectfirst():
        return db.session.query(report).order_by(report.id.desc()).first()

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
    #Let us calculate the amount of water necessary for the crops to grow
    waterPerArea = db.Column(db.Integer())
    #First array element will be the min value and the second one the max value and the third optimal value
    temperatureRange = db.Column(db.ARRAY(db.Float))
    humidityRange = db.Column(db.ARRAY(db.Float))
    soilmoistureRange = db.Column(db.ARRAY(db.Float))
    soiltemperatureRange = db.Column(db.ARRAY(db.Float))
    precipitationRange = db.Column(db.ARRAY(db.Float))
    radiationRange = db.Column(db.ARRAY(db.Float))
    windvelocityRange = db.Column(db.ARRAY(db.Float)) 
    #Money related section
    pricePerKg = db.Column(db.Float())

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

"""
This table is needed because for each report one image per layer will be generated, 
so a report can have several layers of mundi associated with it. 
It should have a one-to-many relationship with the report table.
"""
class mundiImg(db.Model):
    __tablename__ = 'tbl_mundi'
    id = db.Column(db.Integer(), primary_key=True)
    report_id = db.Column(db.Integer(), db.ForeignKey('tbl_reports.id', ondelete='CASCADE'))

    layerName = db.Column(db.String(48))
    url = db.Column(db.String(500))
    colorCount = db.Column(db.ARRAY(db.Integer))
    pixelColor = db.Column(db.ARRAY(db.String(8)))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def getJson(self):
        json = {
            'layerName':self.layerName,
            'url': self.url,
            'colorCount': self.colorCount[0],
            'pixelColor': self.pixelColor[0],
            }
        return json
    
    def getAllJson():
        mundiImgs = report.query.all()
        all = {'mundiImgs': []}
        for e in mundiImgs:
            all['mundiImgs'].append(e.getJson())
        return all
