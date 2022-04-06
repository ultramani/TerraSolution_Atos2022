from enum import unique
from math import fabs
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
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

    #Función que indica a python como imprimir los objetos d e esta clase
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

# class temperature(db.model):
#     __tablename__='tbl_average_temperature_past7years'

#     id = db.Column(db.Integer, primary_key=True)
#     comunidad = db.Column(db.String(128),unique=True)
#     January = db.Column(db.integer, nullable = False)
#     February = db.Column(db.integer, nullable = False)
#     March = db.Column(db.integer, nullable = False)
#     April = db.Column(db.integer, nullable = False)
#     May = db.Column(db.integer, nullable = False)
#     June = db.Column(db.integer, nullable = False)
#     July = db.Column(db.integer, nullable = False)
#     August = db.Column(db.integer, nullable = False)
#     September = db.Column(db.integer, nullable = False)
#     October = db.Column(db.integer, nullable = False)
#     November = db.Column(db.integer, nullable = False)
#     December = db.Column(db.integer, nullable = False)

#     def __init__(self,comunidad,j,f,m,a,ma,ju,jul,au,s,o,n,d):
#             self,comunidad = comunidad
#             self.January = j
#             self.February = f
#             self.March = m
#             self.April = a
#             self.May = ma
#             self.June = ju
#             self.July = jul
#             self.August = au
#             self.September = s
#             self.October = o
#             self.November = n
#             self.December = d

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
        
#     def update(self):
#         db.session.commit()

# class precipitation(db.model):
#     __tablename__='tbl_average_precipitation_past7years'

#     id = db.Column(db.Integer, primary_key=True)
#     comunidad = db.Column(db.String(128),unique=True)
#     January = db.Column(db.integer, nullable = False)
#     February = db.Column(db.integer, nullable = False)
#     March = db.Column(db.integer, nullable = False)
#     April = db.Column(db.integer, nullable = False)
#     May = db.Column(db.integer, nullable = False)
#     June = db.Column(db.integer, nullable = False)
#     July = db.Column(db.integer, nullable = False)
#     August = db.Column(db.integer, nullable = False)
#     September = db.Column(db.integer, nullable = False)
#     October = db.Column(db.integer, nullable = False)
#     November = db.Column(db.integer, nullable = False)
#     December = db.Column(db.integer, nullable = False)

#     def __init__(self,j,f,m,a,ma,ju,jul,au,s,o,n,d):
#             self.January = j
#             self.February = f
#             self.March = m
#             self.April = a
#             self.May = ma
#             self.June = ju
#             self.July = jul
#             self.August = au
#             self.September = s
#             self.October = o
#             self.November = n
#             self.December = d

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
        
#     def update(self):
#         db.session.commit()