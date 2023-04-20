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
    birthday = db.Column(db.String(120))
    avatar_url = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    profession = db.Column(db.String(120))
    address = db.Column(db.String(120))

    def __init__(self, username, email, password, is_admin, active=True):
        # self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.active = active
        self.is_admin = is_admin

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

    # <!--------------chat---------->

    @classmethod
    def get_all(cls):
        return User.query.all()

    # <!--------------chat---------->



    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def isAdmin(self):
        return self.is_admin

    def get_username(self):
        return self.username




class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())


class Destination(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String



class Target(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)  # name is String
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    location = db.Column(db.String(120))
    image = db.Column(db.String(120))
    intro = db.Column(db.String(240))
    # time of duration
    length = db.Column(db.String(240))
    # including 3 types:
    # attraction: 0,
    # accommodation: 1,
    # traffic: 2
    type = db.Column(db.INTEGER)
    price = db.Column(db.INTEGER)

    def __init__(self, name, destination_id, image, intro, type, price):
        self.name = name
        self.destination_id = destination_id
        self.location = Destination.query.filter_by(id=destination_id).first().name
        self.image = image
        self.intro = intro
        self.type = type
        self.price = price



class Day(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    destination_id = db.Column(db.INTEGER, db.ForeignKey('destination.id'))
    attraction_id = db.Column(db.INTEGER, db.ForeignKey('target.id'))
    accommodation_id = db.Column(db.INTEGER, db.ForeignKey('target.id'))
    traffic_id = db.Column(db.INTEGER, db.ForeignKey('target.id'))


class Combination(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(120))
    # max: 7 days
    day1 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day2 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day3 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day4 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day5 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day6 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    day7 = db.Column(db.INTEGER, db.ForeignKey('day.id'))
    intro = db.Column(db.String(240))
    price = db.Column(db.INTEGER)
    length = db.Column(db.INTEGER, nullable=False)
    image = db.Column(db.String(120))

    def __init__(self, name, intro, price, length, image, day1, day2, day3, day4, day5, day6, day7):
        self.name = name
        self.day1 = day1
        self.day2 = day2
        self.day3 = day3
        self.day4 = day4
        self.day5 = day5
        self.day6 = day6
        self.day7 = day7
        self.intro = intro
        self.price = price
        self.length = length
        self.image = image

    def get_days(self):
        days = []
        if self.day1:
            days.append(self.day1)
        if self.day2:
            days.append(self.day2)
        if self.day3:
            days.append(self.day3)
        if self.day4:
            days.append(self.day4)
        if self.day5:
            days.append(self.day5)
        if self.day6:
            days.append(self.day6)
        if self.day7:
            days.append(self.day7)
        print(days)
        return days


# combination record, staff can operate and store data in this table
class RecordC(db.Model):
    __tablename__ = "record_c"
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    combination_id = db.Column(db.INTEGER, db.ForeignKey('combination.id'))
    # record constructed time
    time = db.Column(db.String(120))
    # This scheduled start and end time
    start_time = db.Column(db.String(120))
    # end_time = db.Column(db.String(120))
    # the number of reserved persons
    num = db.Column(db.INTEGER, nullable=False, default=1)
    # the reservation person's name
    name = db.Column(db.String(64))
    # the reservation person's cell phone number
    tel = db.Column(db.String(64))
    status = db.Column(db.String(120))
    price = db.Column(db.INTEGER)



# personal record of attraction, traffic, and accommodation, customer can operate and store data in this table
class Record(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    target_id = db.Column(db.INTEGER, db.ForeignKey('target.id'))
    # record constructed time
    time = db.Column(db.String(120))
    # This scheduled start and end time
    start_time = db.Column(db.String(120))
    # end_time = db.Column(db.String(120))
    # the number of reserved persons
    num = db.Column(db.INTEGER,nullable=False, default =1)
    # the reservation person's name
    name = db.Column(db.String(64))
    # the reservation person's cell phone number
    tel = db.Column(db.String(64))
    status = db.Column(db.String(120))


class FavoriteC(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    combination_id = db.Column(db.INTEGER, db.ForeignKey('combination.id'))
    # collect constructed time
    time = db.Column(db.String(120))


# personal record of attraction, traffic, and accommodation, customer can operate and store data in this table
class Favorite(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    target_id = db.Column(db.INTEGER, db.ForeignKey('target.id'))
    # collect constructed time
    time = db.Column(db.String(120))

# Comments on combination
class CommentC(db.Model):
    __tablename__ = "comment_c"
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    username = db.Column(db.String(120))
    combination_id = db.Column(db.INTEGER, db.ForeignKey('combination.id'))
    # score: 0-5
    score = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.String(240))
    # image if necessary
    image = db.Column(db.String(120))
    # construct time
    time = db.Column(db.String(120))
    # the number of this post to be liked
    like = db.Column(db.INTEGER, default=0)

    # reply_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))  # can be nullable
    # # Whether this comment is a reply to the user
    # # 0: no 1:yes
    # reply_status = db.Column(db.INTEGER, default=0)
    # time2 = db.Column(db.String(120))


# Comments on attraction, traffic, and accommodation
class Comment(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    target_id = db.Column(db.INTEGER, db.ForeignKey('target.id'))
    # score: 0-5
    score = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.String(240))
    # image if necessary
    image = db.Column(db.String(120))
    time = db.Column(db.String(120))
    # the number of this post to be liked
    like = db.Column(db.INTEGER, default=0)


# Users reply on comments of combination
class ReplyC(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    comment_id = db.Column(db.INTEGER, db.ForeignKey('comment_c.id'))
    content = db.Column(db.String(240))
    time = db.Column(db.String(120))
    # the number of this post to be liked
    like = db.Column(db.INTEGER, default=0)


# Users reply on comments of attraction, traffic, and accommodation
class Reply(db.Model):
    __table_args__ = {'extend_existing': True}
    # id is the primary key and it increments automatically
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    comment_id = db.Column(db.INTEGER, db.ForeignKey('comment.id'))
    content = db.Column(db.String(240))
    time = db.Column(db.String(120))
    # the number of this post to be liked
    like = db.Column(db.INTEGER, default=0)

class ContactModel(db.Model):
    __tablename__ = "contact_us"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    message = db.Column(db.String(500))
    create_time = db.Column(db.DateTime, default=datetime.now())

