from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app
from travelAgent.forms import LoginForm, DayTripForm
from travelAgent.models import User, Destination, Target, Day
from travelAgent.views.login_handler import login_manager

staff_blueprint = Blueprint(name="staff_site", import_name=__name__)

day_trip_draft = []
save_draft = False


@staff_blueprint.route('/staff/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    return render_template('./staff_site/index.html')


@staff_blueprint.route('/staff', methods=['GET', 'POST'])
def login():
    print('login')
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
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    logout_user()
    return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff/contents', methods=['GET', 'POST'])
def contents():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    return render_template('./staff_site/contents.html')


@staff_blueprint.route('/staff/contents/new_plan', methods=['GET', 'POST'])
def new_plan():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))

    form = DayTripForm(request.form)
    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    return render_template('./staff_site/new_plan.html', form=form, days=day_trip_draft,
                           destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics)


@staff_blueprint.route('/staff/contents/add', methods=['GET', 'POST'])
def add_new_day():
    form = DayTripForm(request.form)
    if form.validate_on_submit():
        destination = form.destination.data
        attraction = form.attraction.data
        accommodation = form.accommodation.data
        traffic = form.traffic.data
        if day_trip_draft.__len__() < 7:
            day_num = day_trip_draft.__len__() + 1
            day_trip_draft.append([day_num, destination, attraction, accommodation, traffic])
    return redirect(url_for("staff_site.new_plan"))


@staff_blueprint.route('/staff/contents/get_day_num', methods=['GET', 'POST'])
def get_day_num():
    return str(day_trip_draft.__len__())


@staff_blueprint.route('/staff/contents/clear', methods=['GET', 'POST'])
def clear_draft():
    day_trip_draft.clear()
    return redirect(url_for("staff_site.new_plan"))


@staff_blueprint.route('/staff/contents/submit_plan', methods=['GET', 'POST'])
def submit_plan():
    # for day in day_trip_draft:
    #     day = Day(day[0], day[1], day[2], day[3], day[4])
    return redirect(url_for("staff_site.new_plan"))

@login_manager.user_loader
def load_user(id):
    return User.get(int(id))