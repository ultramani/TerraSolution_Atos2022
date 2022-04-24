import matplotlib
import matplotlib.pyplot as plt
from flask_login import LoginManager
from .databaseManager import setup_db, db_drop_and_create_all,db
from .config import APP_CONFIG
from flask_cors import CORS
from flask import Flask
from flask_migrate import Migrate



matplotlib.use('Agg')
app = Flask(__name__, template_folder='templates')
#Nos permite cambiar la configuracion con solo cambiar el string
app.config.from_object(APP_CONFIG["deploy"])
#Login manager, manages the login requests
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#Inicializa la bbdd
setup_db(app)
#Comentar si se quiere persistencia
db_drop_and_create_all()
#Añade protecion contra ataques CORS
CORS(app)
migrate = Migrate(app, db)


from .views import *

