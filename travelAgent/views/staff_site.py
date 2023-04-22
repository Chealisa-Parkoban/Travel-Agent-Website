import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app, db
# from travelAgent.app import changeBookingStatus
from travelAgent.forms import LoginForm, DayTripForm, PlanForm, DestinationForm, TargetForm
from travelAgent.models import User, Destination, Target, Day, Combination
from travelAgent.views.login_handler import login_manager

from travelAgent.config import basedir

staff_blueprint = Blueprint(name="staff_site", import_name=__name__)

day_trip_draft = []
save_draft = False
trip_fees = []


# --------------------chat----------------->
@staff_blueprint.route('/staff/chat')
def chat():
    # changeBookingStatus()
    return render_template('./staff_site/pages/chat.html', user=current_user)


# --------------------chat----------------->

@staff_blueprint.route('/staff/index', methods=['GET', 'POST'])
def index():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    return render_template('./staff_site/index.html', user=current_user)


@staff_blueprint.route('/staff', methods=['GET', 'POST'])
def login():
    # changeBookingStatus()
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
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    logout_user()
    return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff/contents/all_plans', methods=['GET', 'POST'])
def contents():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    plans = Combination.query.all()
    return render_template('./staff_site/all_plans.html', plans=plans, user=current_user)


@staff_blueprint.route('/staff/contents/new_plan', methods=['GET', 'POST'])
def new_plan():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))

    day_form = DayTripForm(request.form)
    plan_form = PlanForm(request.form)
    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    fees = 0
    for fee in trip_fees:
        fees += fee

    return render_template('./staff_site/new_plan.html', day_form=day_form, plan_form=plan_form, days=day_trip_draft,
                           destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, trip_fees=fees, user=current_user)


@staff_blueprint.route('/staff/contents/add', methods=['GET', 'POST'])
def add_new_day():
    # changeBookingStatus()
    form = DayTripForm(request.form)
    if form.validate_on_submit():
        destination = form.destination.data
        attraction = form.attraction.data
        accommodation = form.accommodation.data
        traffic = form.traffic.data
        if day_trip_draft.__len__() < 7:
            day_num = day_trip_draft.__len__() + 1
            day_trip_draft.append([day_num, destination, attraction, accommodation, traffic])

            attraction = Target.query.filter_by(name=attraction).first()
            accommodation = Target.query.filter_by(name=accommodation).first()
            traffic = Target.query.filter_by(name=traffic).first()

            print(attraction.price)
            trip_fees.append(attraction.price)
            trip_fees.append(accommodation.price)
            trip_fees.append(traffic.price)

            print(trip_fees)
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
    # changeBookingStatus()
    name = request.form.get('name')
    intro = request.form.get('intro')
    price = request.form.get('price')
    length = day_trip_draft.__len__()
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
    print(path)

    for day in day_trip_draft:
        destination_id = Destination.query.filter_by(name=day[1]).first().id
        attraction_id = Target.query.filter_by(name=day[2]).first().id
        accommodation_id = Target.query.filter_by(name=day[3]).first().id
        traffic_id = Target.query.filter_by(name=day[4]).first().id

        day = Day(destination_id=destination_id, attraction_id=attraction_id, accommodation_id=accommodation_id,
                  traffic_id=traffic_id)
        days.append(day)
        db.session.add(day)
    db.session.commit()

    for i in range(0, 7 - len(days)):
        days.append(None)

    days_id = []
    for day in days:
        if day is not None:
            days_id.append(day.id)
        else:
            days_id.append(None)

    combination = Combination(name, intro, price, length, path, days_id[0], days_id[1], days_id[2], days_id[3],
                              days_id[4], days_id[5], days_id[6])
    db.session.add(combination)
    db.session.commit()
    day_trip_draft.clear()
    return redirect(url_for("staff_site.contents"))


@staff_blueprint.route('/staff/contents/delete_day', methods=['GET', 'POST'])
def delete_day():
    # changeBookingStatus()
    # print(request.args.get("day_id"), "delete")
    # data = request.args.get("day_id")
    json = request.json
    print(json)
    print("ddd")
    data = request.get_json()
    day_id = data['day_id']
    print(day_id, "delete")

    # age = data['age']
    day_trip_draft.pop(int(day_id) - 1)
    print(day_trip_draft)
    return "ok"
    # return redirect(url_for("staff_site.new_plan"))


# @staff_blueprint.route('/staff/contents/store_plan_id', methods=['GET', 'POST'])
# def store_plan_id():
#     plan_id = request.args.get("plan_id")
#     session['plan_id'] = plan_id
#     # plan = Combination.query.filter_by(id=plan_id).first()
#     # days = plan.get_days()
#     # print("okok")
#     # view_plan(plan,days)
#     return 'ok'
#     # return render_template('./staff_site/plan_detail.html', plan=plan, days=days, plan_form=PlanForm(), day_form=DayTripForm())
#

@staff_blueprint.route('/staff/contents/view_plan', methods=['GET', 'POST'])
def view_plan():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()
    plan_id = session.get('plan_id')
    # print(plan_id, "plan_id")
    plan = Combination.query.filter_by(id=plan_id).first()
    days_id = plan.get_days()
    days = []
    i = 0
    for day_id in days_id:
        if day_id is not None:
            day = Day.query.filter_by(id=day_id).first()
            print(day.id)
            day_des_id = day.destination_id
            day_att_id = day.attraction_id
            day_acc_id = day.accommodation_id
            day_tra_id = day.traffic_id
            print(day_des_id, day_att_id, day_acc_id, day_tra_id)

            day_destination = db.session.query(Destination).filter(Destination.id == day_des_id).first()
            print("destintion", day_destination)
            day_attraction = db.session.query(Target).filter(Target.id == day_att_id).first()
            print("attraction", day_attraction)
            day_accommodation = db.session.query(Target).filter(Target.id == day_acc_id).first()
            print("accommodation", day_accommodation)
            day_traffic = db.session.query(Target).filter(Target.id == day_tra_id).first()
            print("traffic", day_traffic)

            i += 1
            day = [i, day_destination.name, day_attraction.name, day_accommodation.name, day_traffic.name]
            days.append(day)
    print("days", days)
    return render_template('./staff_site/plan_detail.html', plan=plan, days=days, plan_form=PlanForm(),
                           day_form=DayTripForm(), destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, user=current_user)


@staff_blueprint.route('/staff/contents/delete_plan', methods=['GET', 'POST'])
def delete_plan():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    plan_id = session.get('plan_id')
    plan = Combination.query.filter_by(id=plan_id).first()
    # days_id = plan.get_days()
    # for day_id in days_id:
    #     if day_id is not None:
    #         day = Day.query.filter_by(id=day_id).first()
    #         db.session.delete(day)
    db.session.delete(plan)
    db.session.commit()
    return redirect(url_for("staff_site.contents"))


@staff_blueprint.route('/staff/contents/destinations', methods=['GET', 'POST'])
def destinations():
    # changeBookingStatus()
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    destinations = Destination.query.all()
    form = DestinationForm(request.form)
    if form.validate_on_submit():
        destination = form.destination.data
        if Destination.query.filter_by(name=destination).first() is not None:
            message = 'Destination exist!'
            return render_template('./staff_site/destinations.html', destinations=destinations, form=form,
                                   message=message)
        destination = Destination(name=destination)
        db.session.add(destination)
        db.session.commit()
        return redirect(url_for("staff_site.destinations"))
    return render_template('./staff_site/destinations.html', destinations=destinations, form=form, message=message,user=current_user)


@staff_blueprint.route('/staff/contents/attractions', methods=['GET', 'POST'])
def attractions():
    # changeBookingStatus()
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))

    attractions = Target.query.filter_by(type="0").all()
    destinations = Destination.query.all()

    form = TargetForm(request.form)
    if form.validate_on_submit():
        name = request.form.get('name')
        location = request.form.get('location')
        intro = request.form.get('intro')
        price = request.form.get('price')

        if Target.query.filter_by(name=name).first() is not None:
            return render_template('./staff_site/attractions.html', attractions=attractions,
                                   destinations=destinations, form=form, message='Attraction exist!')

        destination = Destination.query.filter_by(name=location).first()
        attraction = Target(name=name, intro=intro, price=price, type="0", destination_id=destination.id, image="")
        db.session.add(attraction)
        db.session.commit()
        return redirect(url_for("staff_site.attractions"))
    return render_template('./staff_site/attractions.html', attractions=attractions, destinations=destinations,
                           form=form, message=message, user=current_user)


@staff_blueprint.route('/staff/contents/accommodations', methods=['GET', 'POST'])
def accommodations():
    # changeBookingStatus()
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    accommodations = Target.query.filter_by(type="1").all()
    destinations = Destination.query.all()

    form = TargetForm(request.form)
    if form.validate_on_submit():
        name = request.form.get('name')
        location = request.form.get('location')
        intro = request.form.get('intro')
        price = request.form.get('price')

        if Target.query.filter_by(name=name).first() is not None:
            message = 'Accommodation exist!'
            return redirect(url_for("staff_site.accommodations", message=message))

        destination = Destination.query.filter_by(name=location).first()
        accommodation = Target(name=name, intro=intro, price=price, type="1", destination_id=destination.id, image="")
        db.session.add(accommodation)
        db.session.commit()
        return redirect(url_for("staff_site.accommodations"))
    return render_template('./staff_site/accommodations.html', hotels=accommodations, destinations=destinations,
                           form=form, message=message, user=current_user)


@staff_blueprint.route('/staff/contents/traffics', methods=['GET', 'POST'])
def traffics():
    # changeBookingStatus()
    message = ""
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    traffics = Target.query.filter_by(type="2").all()
    destinations = Destination.query.all()

    form = TargetForm(request.form)
    if form.validate_on_submit():
        name = request.form.get('name')
        intro = request.form.get('intro')
        price = request.form.get('price')

        if Target.query.filter_by(name=name).first() is not None:
            message = 'Traffic exist!'
            return redirect(url_for("staff_site.traffics", message=message))

        # destination = Destination.query.filter_by(name=location).first()
        traffic = Target(name=name, intro=intro, price=price, type="2", destination_id=1, image="")
        db.session.add(traffic)
        db.session.commit()
        return redirect(url_for("staff_site.traffics"))
    return render_template('./staff_site/traffics.html', traffics=traffics, destinations=destinations, form=form,
                           message=message, user=current_user)


@staff_blueprint.route('/staff/contents/destinations/delete', methods=['GET', 'POST'])
def delete_destination():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    des_id = int(session.get('des_id'))
    print(des_id)
    destination = Destination.query.filter_by(id=des_id).first()
    db.session.delete(destination)
    db.session.commit()
    return redirect(url_for("staff_site.destinations"))


@staff_blueprint.route('/staff/contents/attractions/delete', methods=['GET', 'POST'])
def delete_attraction():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    attr_id = int(session.get('attr_id'))
    print(attr_id)
    attraction = Target.query.filter_by(id=attr_id).first()
    db.session.delete(attraction)
    db.session.commit()
    return redirect(url_for("staff_site.attractions"))


@staff_blueprint.route('/staff/contents/accommodations/delete', methods=['GET', 'POST'])
def delete_accommodation():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    acc_id = int(session.get('acc_id'))
    print(acc_id)
    accommodation = Target.query.filter_by(id=acc_id).first()
    db.session.delete(accommodation)
    db.session.commit()
    return redirect(url_for("staff_site.accommodations"))


@staff_blueprint.route('/staff/contents/traffics/delete', methods=['GET', 'POST'])
def delete_traffic():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    traffic_id = int(session.get('tra_id'))
    traffic = Target.query.filter_by(id=traffic_id).first()
    db.session.delete(traffic)
    db.session.commit()
    return redirect(url_for("staff_site.traffics"))


@login_manager.user_loader
def load_user(id):
    return User.get(int(id))


@staff_blueprint.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))

    u = db.session.query(User).filter(User.id == current_user.id).first()

    gender = request.form.get('gender')
    birth = request.form.get('date_of_birth')
    profession = request.form.get('profession')
    address = request.form.get('address')

    uid = uuid.uuid1()
    # Images storage path
    file_dir = os.path.join(basedir, "static/upload/")
    # Getting the data transferred from the front end
    files = request.files.getlist('avatar-input')  # Gets the value of myfiles from ajax, of type list
    # path = db.session.query(User.avatar_url).filter(User.id == current_user.id).first()
    path = u.avatar_url
    print(path)

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
    print(path)

    u.avatar_url = path
    u.gender = gender
    u.birthday = birth
    u.profession = profession
    u.address = address
    db.session.commit()
    return redirect(url_for('profile'))
