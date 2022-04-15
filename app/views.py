import json
import os

from flask import (Response, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app

from .algorithm import *
from .databaseManager import db
from .forms import LoginForm, RegistrationForm
from .models import User, parameters


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'tractor.ico',mimetype='image/tractor.icon')
    
@app.route("/map")
@login_required
def maptool():
        longparams = parameters.longnames()
        shortparams = parameters.shortnames()
        size = len(longparams)
        return render_template('map.html', longparams = longparams, shortparams = shortparams, size = size)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

        
@app.route('/login', methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
            return redirect(url_for('/'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)
        
@app.route('/logout')
@login_required
def logout():
        logout_user()
        return redirect('/')

        
@app.route('/report')
@login_required
def reportpage():
    return render_template('dataReport.html')

@app.route("/polygon", methods=['POST'])
def polygon():
    #Parse Json
    data = parse_obj(json.loads(request.data))['Data']
    #Obtain circumscribed rectangle
    coords = getRectangle(data)
    return json.dumps(coords)

@app.route("/nasa", methods=['POST'])
def solarData():
    if request.method == "POST":
        data = parse_obj(json.loads(request.data))['Data']
        solarData= getSolarData(data[0], data[1], data[2])
        return json.dumps(solarData)
    else:
        return Response('Error')
