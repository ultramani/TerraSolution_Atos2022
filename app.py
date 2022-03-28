from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from models import setup_db, User, db_drop_and_create_all, db
from config import APP_CONFIG
from flask_cors import CORS
from forms import LoginForm
import config

import os

def create_app(test_config=None):

    app = Flask(__name__, template_folder='templates')
    #Nos permite cambiar la configuracion con solo cambiar el string
    app.config.from_object(APP_CONFIG["development"])
    #Inicializa la bbdd
    setup_db(app)
    #Añade protecion contra ataques CORS
    CORS(app)
    #Login manager, manages the login requests
    login_manager = LoginManager()
    login_manager.init_app(app)
    #Comentar si se quiere persistencia
    db_drop_and_create_all()

    @login_manager.user_loader
    def load_user(user_id):
        user = User.get(user_id)
        if (user == null):
            return None
        else:
            return user

    @app.route("/")
    def home():
        return render_template('home.html')
    
    @app.route("/map")
    def mapTool():
        return render_template('index.html')

    @app.route("/register", methods=['GET','POST'])
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

    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('/'))
        form = LoginForm()
        if form.validate_on_submit():
            user = get_user(form.email.data)
            if user is not None and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('/')
                return redirect(next_page)
        return render_template('signin.html', form=form)
        
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
