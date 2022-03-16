from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, User, db_drop_and_create_all
from config import APP_CONFIG
from flask_cors import CORS
import config

import os

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates')
    #Nos permite cambiar la configuracion con solo cambiar el string
    app.config.from_object(APP_CONFIG["development"])
    setup_db(app)
    CORS(app)
    #Comentar si se quiere persistencia
    db_drop_and_create_all()

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/signup", methods=['GET','POST'])
    def signup():

        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            if name == '' or password == '':
                return render_template('signup.html', message="Please complete all the fields")

            user = User(name,password)
            user.insert()
            
            return redirect("/", code=302)

        elif request.method == 'GET':
            return render_template('signup.html')

        else:
            return 'Not a valid request method for this route'
    
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT",8443))
    app.run(host='127.0.0.1',port=port,debug=True)
