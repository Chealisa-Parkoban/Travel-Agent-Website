import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app, db
from travelAgent.forms import LoginForm, DayTripForm, PlanForm, DestinationForm, AttractionForm
from travelAgent.models import User, Destination, Target, Day, Combination
from travelAgent.views.login_handler import login_manager

from travelAgent.config import basedir
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
        return render_template('./staff_site/pages/login.html', form=form)
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

    return render_template('./staff_site/pages/login.html', form=form)


@staff_blueprint.route('/staff/logout', methods=['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    logout_user()
    return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff/contents/all_plans', methods=['GET', 'POST'])
def contents():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    plans = Combination.query.all()
    return render_template('./staff_site/all_plans.html', plans=plans)


@staff_blueprint.route('/staff/contents/new_plan', methods=['GET', 'POST'])
def new_plan():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))

    day_form = DayTripForm(request.form)
    plan_form = PlanForm(request.form)
    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    return render_template('./staff_site/new_plan.html', day_form=day_form, plan_form=plan_form, days=day_trip_draft,
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
    name = request.form.get('name')
    intro = request.form.get('intro')
    price = request.form.get('price')
    length = day_trip_draft.__len__()
    print(name, intro, price, length)
    days = []

    uid = uuid.uuid1()
    # Images storage path
    file_dir = os.path.join(basedir, "static/upload/")
    # Getting the data transferred from the front end
    files = request.files.getlist('img')  # Gets the value of myfiles from ajax, of type list
    path = ""

    for img in files:
        # Extract the suffix of the uploaded image and
        # Name the image after the commodity id and store it in the specific path
        check = img.content_type
        # check if upload image
        if str(check) != 'application/octet-stream':
            fname = img.filename
            ext = fname.rsplit('.', 1)[1]
            new_filename = uid.hex + '.' + ext
            img.save(os.path.join(file_dir, new_filename))
            path = "../static/upload/" + new_filename

    # default: like=0 path=""
    print("777777777777777")
    print(path)

    for day in day_trip_draft:
        destination_id = Destination.query.filter_by(name=day[1]).first().id
        attraction_id = Target.query.filter_by(name=day[2]).first().id
        accommodation_id = Target.query.filter_by(name=day[3]).first().id
        traffic_id = Target.query.filter_by(name=day[4]).first().id

        day = Day(destination_id=destination_id, attraction_id=attraction_id, accommodation_id=accommodation_id, traffic_id=traffic_id)
        days.append(day)
        db.session.add(day)
    db.session.commit()

    for i in range(0, 7-len(days)):
        days.append(None)

    days_id = []
    for day in days:
        if day is not None:
            days_id.append(day.id)
        else:
            days_id.append(None)

    combination = Combination(name, intro, price, length, path, days_id[0], days_id[1], days_id[2], days_id[3], days_id[4], days_id[5], days_id[6])
    db.session.add(combination)
    db.session.commit()
    day_trip_draft.clear()
    return redirect(url_for("staff_site.contents"))


@staff_blueprint.route('/staff/contents/delete_day', methods=['GET', 'POST'])
def delete_day():
    # print(request.args.get("day_id"), "delete")
    # data = request.args.get("day_id")
    json = request.json
    print(json)
    print("ddd")
    data = request.get_json()
    day_id = data['day_id']
    print(day_id, "delete")

    # age = data['age']
    day_trip_draft.pop(int(day_id)-1)
    print(day_trip_draft)
    return "ok"
    # return redirect(url_for("staff_site.new_plan"))


@staff_blueprint.route('/staff/contents/plan_detail', methods=['GET', 'POST'])
def plan_detail():
    plan_id = request.args.get("plan_id")
    plan = Combination.query.filter_by(id=plan_id).first()
    days = plan.get_days()
    print("okok")
    view_plan(plan,days)
    return 'ok'
    # return render_template('./staff_site/plan_detail.html', plan=plan, days=days, plan_form=PlanForm(), day_form=DayTripForm())


@staff_blueprint.route('/staff/contents/view_plan', methods=['GET', 'POST'])
def view_plan(plan, days):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    return render_template('./staff_site/plan_detail.html', plan=plan, days=days, plan_form=PlanForm(),
                           day_form=DayTripForm())


# @staff_blueprint.route('/staff/contents/all_contents', methods=['GET', 'POST'])
# def all_contents():
#     if not current_user.is_authenticated:
#         return redirect(url_for("staff_site.login"))
#     destinations = Destination.query.all()
#     attractions = Target.query.filter_by(type="0").all()
#     accommodations = Target.query.filter_by(type="1").all()
#     traffics = Target.query.filter_by(type="2").all()
#     return render_template('./staff_site/destinations.html', destinations=destinations, attractions=attractions,
#                            hotels=accommodations, traffics=traffics)


@staff_blueprint.route('/staff/contents/destinations', methods=['GET', 'POST'])
def destinations():
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    destinations = Destination.query.all()
    form = DestinationForm(request.form)
    if form.validate_on_submit():
        destination = form.destination.data
        print(destination)
        if Destination.query.filter_by(name=destination).first() is not None:
            message = 'Destination exist!'
            return render_template('./staff_site/destinations.html', destinations=destinations, form=form, message=message)
        destination = Destination(name=destination)
        db.session.add(destination)
    db.session.commit()
    return render_template('./staff_site/destinations.html', destinations=destinations, form=form, message=message)


@staff_blueprint.route('/staff/contents/attractions', methods=['GET', 'POST'])
def attractions():
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    attractions = Target.query.filter_by(type="0").all()
    form = AttractionForm(request.form)
    if form.validate_on_submit():
        attraction = form.attraction.data
        if Target.query.filter_by(name=attraction).first() is not None:
            message = 'Attraction exist!'
            return render_template('./staff_site/destinations.html', attractions=attractions, form=form,
                                   message=message)
        # attraction = Target(name=attraction)
        # db.session.add(attraction)
    db.session.commit()
    return render_template('./staff_site/attractions.html', attractions=attractions)


@staff_blueprint.route('/staff/contents/accommodations', methods=['GET', 'POST'])
def accommodations():
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    accommodations = Target.query.filter_by(type="1").all()
    return render_template('./staff_site/accommodations.html', hotels=accommodations)


@staff_blueprint.route('/staff/contents/traffics', methods=['GET', 'POST'])
def traffics():
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    traffics = Target.query.filter_by(type="2").all()
    return render_template('./staff_site/traffics.html', traffics=traffics)


# @staff_blueprint.route('/staff/contents/add_destination', methods=['GET', 'POST'])
# def add_destination():
#
#     return render_template('./staff_site/destinations.html')


@login_manager.user_loader
def load_user(id):
    return User.get(int(id))