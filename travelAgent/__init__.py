from flask import Flask

import travelAgent.config
# from travelAgent.config import Config
# from flask_sqlalchemy import SQLAlchemy

# create variable app
app = Flask(__name__)

# passing all the configuration information from config.py
# app.config.from_object(Config)

# create database for the app
# db = SQLAlchemy(app)


