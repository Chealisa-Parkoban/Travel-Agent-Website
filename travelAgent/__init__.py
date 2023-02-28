from flask import Flask

import travelAgent.config
from travelAgent.config import Config
from flask_sqlalchemy import SQLAlchemy

# create variable app
app = Flask(__name__)
app.secret_key = 'BxeE3wJcjYi6yA7y1bjBJ1IAs0'

# passing all the configuration information from config.py
app.config.from_object(Config)

# create database for the app

db = SQLAlchemy(app)

# Very important!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# from travelAgent import app, models