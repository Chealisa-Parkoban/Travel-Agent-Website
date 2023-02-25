from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from travelAgent import db


# User class inherits from db.Model
# The database form models are defined as follows
# Use these models to create forms in database


# This model stores user's information

class User(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)  # username is String and unique
    email = db.Column(db.String(120), index=True, unique=True)  # user's email must be unique
    password_hash = db.Column(db.String(128))  # User's password must be hash
    website = db.Column(db.String(128))
    title = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    birthday = db.Column(db.INTEGER)
    avatar_url = db.Column(db.String(120))