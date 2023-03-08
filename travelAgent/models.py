from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from travelAgent import db


# User class inherits from db.Model
# The database form models are defined as follows
# Use these models to create forms in database


# This model stores user's information

class UserModel(db.Model):
    __tablename__ = "Users"
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)  # username is String and unique
    email = db.Column(db.String(120), index=True, unique=True)  # user's email must be unique
    password_hash = db.Column(db.String(128))  # User's password must be hash
    # website = db.Column(db.String(128))
    # title = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    birthday = db.Column(db.INTEGER)
    avatar_url = db.Column(db.String(120))

    # protect the string
    @property
    def password(self):
        raise ArithmeticError("password can not be shown")

    # Encrypted passwords
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password
    def verity_password(self, password):
        check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())


class Staff(db.Model):
    # extend_existing = True
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)  # username is String and unique
    email = db.Column(db.String(120), index=True, unique=True)  # user's email must be unique
    password_hash = db.Column(db.String(128))  # User's password must be hash+
    level = db.Column(db.INTEGER, default=0)

    @property
    def password(self):
        raise ArithmeticError("password can not be shown")

    # Encrypted passwords
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password
    def verity_password(self, password):
        check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Staff {}>'.format(self.username)


class Destination(db.Model):
    # extend_existing = True
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String


class Attraction(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    image = db.Column(db.String(120))
    intro = db.Column(db.String(240))
    price = db.Column(db.INTEGER)


class Accommodation(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    type_id = db.Column(db.INTEGER, db.ForeignKey('type.id'))
    price = db.Column(db.INTEGER)


class Traffic(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    origin_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    type_id = db.Column(db.INTEGER, db.ForeignKey('type.id'))
    start_time = db.Column(db.String(120))
    end_time = db.Column(db.String(120))
    price = db.Column(db.INTEGER)


# Including traffic and accommodation type
class Type(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String


# Elements that can be reserved
# Update this table as we add attractions, accommodations, and transportation,
# adding the appropriate ids
class Atom(db.Model):
    # id is the primary key
    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    # 0:attraction 1:accommodation 2:traffic
    form = db.Column(db.INTEGER, nullable=False)


class Booking(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    atom_id = db.Column(db.INTEGER, db.ForeignKey('atom.id'))
    start_date = db.Column(db.String(120))
    end_date = db.Column(db.String(120))
    remind_time = db.Column(db.String(120))
    status = db.Column(db.String(120))


class Comment(db.Model):
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    atom_id = db.Column(db.INTEGER, db.ForeignKey('atom.id'))
    # The type of object the user comments
    # 0:attraction 1:accommodation
    atom_status = db.Column(db.INTEGER, default=0)
    reply_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))  # can be nullable
    # Whether this comment is a reply to the user
    # 0: no 1:yes
    reply_status = db.Column(db.INTEGER, default=0)
    time = db.Column(db.String(120))

