from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__, template_folder='static')
app.config['SECRET KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get("DATABASE_URL")

db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    max_temperature = db.Column(db.Integer)

# db.init_app()

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
