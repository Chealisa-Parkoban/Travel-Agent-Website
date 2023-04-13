from flask import Flask
from flask_mail import Mail

import travelAgent.config
from travelAgent.config import Config
from flask_sqlalchemy import SQLAlchemy

import os

if not os.path.exists("./logs"):
    os.makedirs("./logs")

# create variable app
app = Flask(__name__)
app.secret_key = 'BxeE3wJcjYi6yA7y1bjBJ1IAs0'

# passing all the configuration information from config.py
app.config.from_object(Config)

# create database for the app

db = SQLAlchemy(app)
mail = Mail(app)

# Very important!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from travelAgent import app, models