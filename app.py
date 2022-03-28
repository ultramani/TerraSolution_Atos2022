from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, User, db_drop_and_create_all, db
from config import APP_CONFIG
from flask_cors import CORS
import config
import json
from algorithm import *

import os

def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates')
    #Nos permite cambiar la configuracion con solo cambiar el string
    app.config.from_object(APP_CONFIG["deploy"])
    setup_db(app)
    CORS(app)
    #Comentar si se quiere persistencia
    # db_drop_and_create_all()

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/signup", methods=['GET','POST'])
    def signup():
        #This if/elif decides what to do depending of the request method
        if request.method == 'POST':
            #Maps the data from the form
            name = request.form['name']
            password = request.form['password']
            #Checks if the fields are empty, if is so it returns a message
            if name == '' or password == '':
                return render_template('signup.html', message="Please complete all the fields")
            #Checks if there is an already existing user 
            if db.session.query(User).filter(User.name == name).filter(User.password == password).count() == 0:
                user = User(name,password)
                user.insert()
            
                return redirect("/", code=302)
            else:
                return render_template('signup.html', message="The user already exists")
        elif request.method == 'GET':
            return render_template('signup.html')
        else:
            return 'Not a valid request method for this route'
    
    
    @app.route("/polygon", methods=['POST'])
    def polygon():
        #Parse Json
        data = parse_obj(json.loads(request.data))['Data']
        #Obtain circumscribed rectangle
        coords = getRectangle(data)
        return json.dumps(coords)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
