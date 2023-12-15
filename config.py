from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'fetch.login_post'


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aleks16040@localhost:1604/rpp'
app.config['SQLAlchemy_TRACK_MODIFIVATTION'] = False