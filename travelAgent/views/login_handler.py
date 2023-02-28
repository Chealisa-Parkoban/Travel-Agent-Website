import flask
from flask import Blueprint, request, redirect, url_for, abort
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import check_password_hash

from travelAgent import app
from travelAgent.forms import LoginForm

from travelAgent.models import Users

login_manager = LoginManager()
login_manager.init_app(app)

login_blueprint = Blueprint(name="login", import_name=__name__)


class User(UserMixin):
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return

    @classmethod
    def get(cls, userid):
        pass


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info('Entered LOGIN page')
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        users = Users.query.all()

        for u in users:
            # if username-password pair exists in the database, login successfully
            if u.username == username and check_password_hash(u.password_hash, password):
                login_user(User(u.username, u.password_hash, u.id))
                app.logger.info('User \'' + u.username + '\' has successfully logged into the website')
                return redirect(url_for("index"))

        app.logger.error('Login failed: Wrong username or password')
        return flask.render_template('sign-in.html', form=form)

    return flask.render_template('sign-in.html', form=form)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)
