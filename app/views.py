import json
import os
from urllib import response
from flask import (Response, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import app
from .algorithm import *
from .databaseManager import db
from .forms import LoginForm, RegistrationForm
from .models import User, parameters, report


@app.route("/")
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

        
@app.route('/report', methods=['GET'])
@login_required
def reportpage():
    report_raw = report.selectfirst()
    return render_template('dataReport.html',report=report_raw)



@app.route("/polygon", methods=['POST'])
def polygon():
    #Parse Json
    data = parse_obj(json.loads(request.data))['Data']
    #Obtain circumscribed rectangle
    geoJson = getRectangle(data)
    return json.dumps(geoJson)

@app.route("/report", methods=['POST'])
def solarData():
    if request.method == "POST":
        data = parse_obj(json.loads(request.data))['Data']
        solarData = getSolarData(data['center'][0], data['center'][0], data['params'])
        outputmsg = save(data,solarData)
        saveMundi(data) # Saves mundi data inside BBDD, ejecutar siempre después de save
        return outputmsg
    else:
        return Response('Error')

# Added by isaac
"""@app.route("/VegetationBORRAR")
def vegetation():
    return render_template('VegetationBORRAR.html')"""

#This is a test function to return the json values to create the pie chart
@app.route("/mundiChart", methods=['POST'])
def testMundi():
    if request.method == "POST":
        data = pruebaMundi()
        return data
    else:
        return Response('Error')

# Added by other user 
@app.route("/pdf", methods=['GET'])
def generatePdf():
        response = generatePDF()
        return response   

@app.route("/test", methods=['POST'])
def test():
    if request.method == "POST":
        None        
    else:
        return Response('Error')

