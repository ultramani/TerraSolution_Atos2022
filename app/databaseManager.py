from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()