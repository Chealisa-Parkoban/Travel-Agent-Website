from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app
from travelAgent.forms import LoginForm
from travelAgent.models import User
from travelAgent.views.login_handler import login_manager

staff_blueprint = Blueprint(name="staff_site", import_name=__name__)


def check_login():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff/index', methods=['GET', 'POST'])
def index():
    check_login()
    return render_template('./staff_site/index.html')


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
                return redirect(url_for("staff_site.login", form=form, message=emsg))
            elif not user.isAdmin():
                emsg = "You are not a staff!"
                app.logger.error('Login failed: You are not a staff!')
                return redirect(url_for("staff_site.login", form=form, message=emsg))
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
    check_login()
    logout_user()
    return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff/contents', methods=['GET', 'POST'])
def contents():
    check_login()
    return render_template('./staff_site/contents.html')


@staff_blueprint.route('/staff/contents/new_plan', methods=['GET', 'POST'])
def new_plan():
    check_login()
    print("new_plan")
    return render_template('./staff_site/new_plan.html')


@login_manager.user_loader
def load_user(id):
    return User.get(int(id))