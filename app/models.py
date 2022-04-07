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
     #Monthly
     avgMonthlytemperature = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlyprecipitation = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlyhumidity = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlysoilmoisture = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgMonthlyradiation = db.Column(db.ARRAY(db.Integer, dimensions=12))
     #Annual
     avgAnnualtemperature = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgAnnualprecipitation = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgAnnualhumidity = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgAnnualsoilmoisture = db.Column(db.ARRAY(db.Integer, dimensions=12))
     avgAnnualradiation = db.Column(db.ARRAY(db.Integer, dimensions=12))

     def insert(self):
        db.session.add(self)
        db.session.commit()

     def delete(self):
        db.session.delete(self)
        db.session.commit()
        
     def update(self):
        db.session.commit()


