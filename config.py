import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    DEVELOPMENT = True
    DEBUG = True

    # database_name ='terraSolutions'
    # default_database_path= "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
    # database_path = os.getenv('DATABASE_URL', default_database_path)
    # SQLALCHEMY_DATABASE_URI = database_path

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/terraSolution'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class StagingConfig(DevelopmentConfig):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(DevelopmentConfig):
    TESTING = True

class DeployConfig(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://ebpehgztisvaai:19c46e5d58fabf2b507750f5bba064453e88b1509066855adeae9290613c3ec4@ec2-52-214-125-106.eu-west-1.compute.amazonaws.com:5432/d28gvf0u07b7g9'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "deploy": DeployConfig
}