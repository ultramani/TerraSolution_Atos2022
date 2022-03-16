import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    DEVELOPMENT = True
    DEBUG = True

    database_name ='terraSolutions'
    default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path)
    SQLALCHEMY_DATABASE_URI = database_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class StagingConfig(DevelopmentConfig):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(DevelopmentConfig):
    TESTING = True

APP_CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig
}