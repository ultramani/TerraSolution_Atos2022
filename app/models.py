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
     location  = db.Column(db.ARRAY(db.Integer, dimensions=4),nullable=False)
     areaSquareHectare = db.Column(db.Integer())

     #Monthly data
     avgMonthlytemperature = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlyprecipitation = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlyhumidity = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlysoilmoisture = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlyradiation = db.Column(db.ARRAY(db.Integer, dimensions=12))
     #Annual data
     avgAnnualtemperature = db.Column(db.Integer())
     avgAnnualprecipitation = db.Column(db.Integer())
     avgAnnualhumidity = db.Column(db.Integer())
     avgAnnualsoilmoisture = db.Column(db.Integer())
     avgAnnualradiation = db.Column(db.Integer())
     #Money wise data
     avgTotalIncome = db.Column(db.Integer())
     avgHectareIncome = db.Column(db.Integer())
     avgPricePerKg = db.Column(db.Integer())
     avgKgPerHectare = db.Column(db.Integer())
     #Algorithm outcome data
     temperature = db.Column(db.Integer())
     humidity = db.Column(db.Integer())
     precipitation = db.Column(db.Integer())
     soilmoisture = db.Column(db.Integer())
     radiation = db.Column(db.Integer())
     
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
    #Add a custom domain [tree, bush , grass]
    cropType = db.Column(db.String(128),nullable=False)
    #First array element will be the min value and the second one the max value and the third optimal value
    temperatureRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    humidityRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    soilmoistureRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    precipitationRange = db.Column(db.ARRAY(db.Integer, dimensions=3))
    radiationRange = db.Column(db.ARRAY(db.Integer, dimensions=3))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
