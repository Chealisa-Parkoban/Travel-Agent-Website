import flask
from flask import Blueprint, request, redirect, url_for, abort, flash, render_template
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from travelAgent import app, db
from travelAgent.forms import LoginForm, SignupForm

from travelAgent.models import User

login_manager = LoginManager()
login_manager.init_app(app)

login_blueprint = Blueprint(name="account", import_name=__name__)


class my_user(UserMixin):
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
        users = User.query.all()

        for u in users:
            # if username-password pair exists in the database, login successfully
            if u.username == username and check_password_hash(u.password_hash, password):
                login_user(my_user(u.username, u.password_hash, u.id))
                app.logger.info('User \'' + u.username + '\' has successfully logged into the website')
                return redirect(url_for("index"))

        app.logger.error('Login failed: Wrong username or password')
        return render_template('sign-in.html', form=form)

    return render_template('sign-in.html', form=form)


@login_blueprint.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    app.logger.info('Entered SIGN UP page')
    # form = SignupForm()
    form = SignupForm(request.form)

    if form.validate_on_submit():
        app.logger.info('Sign up form information get')
        # get user's information
        newname = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_hash = generate_password_hash(password)

        # session['userExist'] = 'false'
        # store user's information into database
        u1 = User(username=newname, email=email, password_hash=password_hash)
        db.session.add(u1)
        db.session.commit()
        app.logger.info('User \'' + newname + '\' has successfully signed up')

        # flash the message
        flash('Signup requested for user {}'.format(form.username.data))
        # redirect to the login page, for user to login
        return redirect(url_for("account.login"))
    else:
        app.logger.error('Sign up information not valid.')

    return render_template('customer_register.html', title='sign-up', form=form)


@login_manager.user_loader
def load_user(userid):
    return my_user.get(userid)