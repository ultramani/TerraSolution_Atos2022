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
    
    #Datos obtenidos
    params = db.Column(JSON)
    #Datos del analisis
        #Numero de palntas a las que le hemso dado el ok
    numberOfPlants = db.Column(db.Integer())
        #Media de los datos de los x meses por planta, en la posición cero se enccuentra el id del parametro
    avgMonthlyTemperaturePlants = db.Column(db.ARRAY(db.Float))
    avgMonthlyPrecipitationPlants = db.Column(db.ARRAY(db.Float))
    avgMonthlyHumidityPlants = db.Column(db.ARRAY(db.Float))
    avgMonthlySoilmoisturePlants = db.Column(db.ARRAY(db.Float))
    avgMonthlySoiltemperaturePlants = db.Column(db.ARRAY(db.Float))
    avgMonthlyRadiationPlants = db.Column(db.ARRAY(db.Float))
    avgMonthlyWindVelocityPlants = db.Column(db.ARRAY(db.Float))
        #Puntuaciones de plantas
    plantsScores = db.Column(db.ARRAY(db.Integer))
    plantsNames = db.Column(db.ARRAY(db.String))
    plantsBadges = db.Column(db.ARRAY(db.String))
    plantsLifePeriod = db.Column(db.ARRAY(db.Integer))
    
    priceperkg = db.Column(db.ARRAY(db.Float)) 
    waterneeded = db.Column(db.ARRAY(db.Float))
    watercost = db.Column(db.ARRAY(db.Float))
    benefit = db.Column(db.ARRAY(db.Float))
    
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
    
    def selectreportbyid(id):
        return db.session.query(report).filter_by(id=id).first()

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return self.id

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
    timetogrowmonths= db.Column(db.Integer(), nullable=False)
    #Nuemro de plantas plantables por hectarea.
    densityOfPopulation = db.Column(db.Integer())
    #Add a custom domain [tree, bush , grass]
    cropType = db.Column(db.String(128),nullable=False)
    #Let us calculate the amount of water necessary for the crops to grow
    waterPerArea = db.Column(db.Float())
    waterperiod = db.Column(db.Integer)
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
    kgspersqm = db.Column(db.Float())
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()

    def getNames():
        raw_data = db.session.query(crop.name).all()
        data = [i[0] for i in raw_data]
        return data
    
    def getrange(id,param):
        if param == "T2M":
            range_raw = db.session.query(crop.temperatureRange).filter_by(id=id).first()
        elif param == 'RH2M':
            range_raw = db.session.query(crop.humidityRange).filter_by(id=id).first()
        elif param == 'ALLSKY_SFC_PAR_TOT':
            range_raw = db.session.query(crop.radiationRange).filter_by(id=id).first()
        elif param == 'PRECTOTCORR':
            range_raw = db.session.query(crop.precipitationRange).filter_by(id=id).first()
        elif param == 'TS':
            range_raw = db.session.query(crop.soiltemperatureRange).filter_by(id=id).first()
        elif param == 'GWETPROF':
            range_raw = db.session.query(crop.soilmoistureRange).filter_by(id=id).first()
        elif param == 'WS2M':
            range_raw = db.session.query(crop.windvelocityRange).filter_by(id=id).first()
        else:
            return None
        rangex = range_raw[0]
        return rangex
    
    def growthrange(id):
        rangex = db.session.query(crop.timetogrowmonths).filter_by(id=id).first()
        rangex = rangex[0]
        return rangex
    
    def getwaterneed(id):
        data = []
        raw_data = db.session.query(crop.waterPerArea).filter_by(id=id).first()
        data.append(raw_data[0])
        raw_data = db.session.query(crop.waterperiod).filter_by(id=id).first()
        data.append(raw_data[0])
        return data
    
    def getallyields():
        raw_data = db.session.query(crop.kgspersqm).all()
        data = [i[0] for i in raw_data] 
        return data 
    
    def getallprices():
        raw_data = db.session.query(crop.pricePerKg).all()
        data = [i[0] for i in raw_data]  
        return data 
    
    def getalllifeperiods():
        raw_data = db.session.query(crop.timetogrowmonths).all()
        data = [i[0] for i in raw_data]  
        return data 