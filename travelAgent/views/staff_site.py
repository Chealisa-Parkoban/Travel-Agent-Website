from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app
from travelAgent.forms import LoginForm
from travelAgent.models import User

staff_blueprint = Blueprint(name="staff_site", import_name=__name__)


@staff_blueprint.route('/staff/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('./staff_site/pages/index/index.html')
    return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff', methods=['GET', 'POST'])
def login():
    global emsg
    app.logger.info('Entered STAFF LOGIN page')
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('./staff_site/pages/samples/login.html', form=form)
    else:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            user = User.get_by_username(username)
            if user is None:
                emsg = "Username not exist!"
                return render_template('./staff_site/pages/samples/login.html', form=form, message=emsg)
            elif not user.isAdmin():
                emsg = "You are not a staff!"
                app.logger.error('Login failed: You are not a staff!')
                return render_template('./staff_site/pages/samples/login.html', form=form, message=emsg)
            else:
                if user.verify_password(password):
                    login_user(user, remember=remember_me)
                    emsg = "STAFF Login successfully!"
                    app.logger.info('Staff \'' + username + '\' has successfully logged into the website')
                    return redirect(url_for("staff_site.index"))
        else:
            emsg = "Wrong password!"
            app.logger.error('Login failed: Wrong username or password')

    return render_template('./staff_site/pages/samples/login.html', form=form)


@staff_blueprint.route('/staff/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("staff_site.login"))

@staff_blueprint.route('/staff/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('./background/dashboard.html')