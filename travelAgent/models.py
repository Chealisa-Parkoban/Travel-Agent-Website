from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import cryptography

from travelAgent import db


# User class inherits from db.Model
# The database form models are defined as follows
# Use these models to create forms in database


# This model stores user's information

class User(UserMixin, db.Model):
    __tablename__ = "user"
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
    active = db.Column(db.Boolean, default=True)


    def __init__(self, username, email, password, active=True):
        # self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.active = active

    # protect the string
    @property
    def password(self):
        raise ArithmeticError("password can not be shown")

    # Encrypted passwords
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_auth_token(self):
        return

    @classmethod
    def get(cls, userid):
        return User.query.filter_by(id=userid).first()

    def get_by_username(username):
        return User.query.filter_by(username=username).first()



class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())


class Staff(db.Model):
    __table_args__ = {'extend_existing': True}
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
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String


class Attraction(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    image = db.Column(db.String(120))
    intro = db.Column(db.String(240))
    # various period are different which has different id
    start_time = db.Column(db.String(120))
    end_time = db.Column(db.String(120))
    price = db.Column(db.INTEGER)


class Accommodation(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    type_id = db.Column(db.INTEGER, db.ForeignKey('type.id'))
    price = db.Column(db.INTEGER)


class Traffic(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    origin_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    type_id = db.Column(db.INTEGER, db.ForeignKey('type.id'))
    start_time = db.Column(db.String(120))
    end_time = db.Column(db.String(120))
    price = db.Column(db.INTEGER)


# Including traffic and accommodation type // can be deleted
class Type(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String


# Elements that can be reserved
# Update this table as we add attractions, accommodations, and transportation,
# adding the appropriate ids
# class Atom(db.Model):
#     # id is the primary key
#     id = db.Column(db.INTEGER, primary_key=True, nullable=False)
#     # 0:attraction 1:accommodation 2:traffic
#     form = db.Column(db.INTEGER, nullable=False)


class Day(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    attraction_id = db.Column(db.INTEGER, db.ForeignKey('attraction.id'))
    accommodation_id = db.Column(db.INTEGER, db.ForeignKey('accommodation.id'))
    traffic_id = db.Column(db.INTEGER, db.ForeignKey('traffic.id'))


class Combination(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    # max: 7 days
    day1 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day2 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day3 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day4 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day5 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day6 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day7 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    length = db.Column(db.INTEGER, nullable=False)



# combination record, staff can operate and store data in this table
class RecordC(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    combination_id = db.Column(db.INTEGER, db.ForeignKey('combination.id'))
    status = db.Column(db.String(120))


# personal record of attraction, customer can operate and store data in this table
class RecordA(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    attraction_id = db.Column(db.INTEGER, db.ForeignKey('attraction.id'))
    date = db.Column(db.String(120))
    status = db.Column(db.String(120))


# personal record of traffic, customer can operate and store data in this table
class RecordT(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    traffic_id = db.Column(db.INTEGER, db.ForeignKey('traffic.id'))
    start_date = db.Column(db.String(120))
    end_date = db.Column(db.String(120))
    status = db.Column(db.String(120))


# personal record of hotel(accommodation), customer can operate and store data in this table
class RecordH(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    accommodation_id = db.Column(db.INTEGER, db.ForeignKey('accommodation.id'))
    date = db.Column(db.String(120))
    status = db.Column(db.String(120))


# Comments on combination
class CommentC(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    combination_id = db.Column(db.INTEGER, db.ForeignKey('combination.id'))
    # score: 0-5
    score = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.String(240))
    # image if necessary
    image = db.Column(db.String(120))
    time = db.Column(db.String(120))
    # the number of this post to be replied
    count = db.Column(db.INTEGER, default = 0)

    reply_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))  # can be nullable
    # Whether this comment is a reply to the user
    # 0: no 1:yes
    reply_status = db.Column(db.INTEGER, default=0)
    time2 = db.Column(db.String(120))


# Comments on attraction
class CommentA(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    attraction_id = db.Column(db.INTEGER, db.ForeignKey('attraction.id'))
    # score: 0-5
    score = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.String(240))
    # image if necessary
    image = db.Column(db.String(120))
    time = db.Column(db.String(120))
    # the number of this post to be replied
    count = db.Column(db.INTEGER, default = 0)


# Comments on hotel (accommodation
class CommentH(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    accommodation_id = db.Column(db.INTEGER, db.ForeignKey('accommodation.id'))
    # score: 0-5
    score = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.String(240))
    # image if necessary
    image = db.Column(db.String(120))
    time = db.Column(db.String(120))
    # the number of this post to be replied
    count = db.Column(db.INTEGER, default = 0)


# Users reply on comments of combination
class ReplyC(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    comment_id = db.Column(db.INTEGER, db.ForeignKey('comment_c.id'))
    content = db.Column(db.String(240))
    time = db.Column(db.String(120))


# Users reply on comments of attraction
class ReplyA(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    comment_id = db.Column(db.INTEGER, db.ForeignKey('comment_a.id'))
    content = db.Column(db.String(240))
    time = db.Column(db.String(120))


# Users reply on comments of hotel (accommodation
class ReplyH(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    comment_id = db.Column(db.INTEGER, db.ForeignKey('comment_h.id'))
    content = db.Column(db.String(240))
    time = db.Column(db.String(120))