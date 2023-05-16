import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app, db
# from travelAgent.app import changeBookingStatus
from travelAgent.forms import LoginForm, DayTripForm, PlanForm, DestinationForm, TargetForm
from travelAgent.models import User, Destination, Target, Day, Combination, RecordC, Record, ContactModel, \
    UserCombination, CommentC, FavoriteC, RecordP, Comment, Favorite
from travelAgent.views.login_handler import login_manager

from travelAgent.config import basedir

staff_blueprint = Blueprint(name="staff_site", import_name=__name__)

day_trip_draft = []
customised_day_trip_draft = []
customised_update_trip_draft = []
save_draft = False
customised_save_draft = False
trip_fees = []
customised_trip_fees = []


# --------------------chat----------------->
@staff_blueprint.route('/staff/chat')
def chat():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    # changeBookingStatus()
    return render_template('./staff_site/pages/chat.html', user=current_user)


# --------------------chat----------------->

@staff_blueprint.route('/staff/index', methods=['GET', 'POST'])
def index():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    combinations = Combination.query.all()
    targets = Target.query.all()
    # merge two list combinations and targets into one list items
    items = []
    for combination in combinations:
        items.append(combination)
    for target in targets:
        items.append(target)
    return render_template('./staff_site/index.html', user=current_user, items=items)


@staff_blueprint.route('/staff/get_data', methods=['GET', 'POST'])
def get_data():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    combinations = Combination.query.all()
    targets = Target.query.all()
    # merge two list combinations and targets into one list items
    items = []
    for combination in combinations:
        items.append(combination)
    for target in targets:
        items.append(target)
    return items


@staff_blueprint.route('/staff', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/', methods=['GET', 'POST'])
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
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    logout_user()
    return redirect(url_for("staff_site.login"))


@staff_blueprint.route('/staff/contents/all_plans', methods=['GET', 'POST'])
def contents():
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plans = Combination.query.all()
    return render_template('./staff_site/all_plans.html', plans=plans, user=current_user)


@staff_blueprint.route('/staff/pack_load_detail', methods=['GET', 'POST'])
def pack_load_detail():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plan_id_res = request.args.get("plan_id_res")

    plan = db.session.query(Combination).filter_by(id=plan_id_res).first()
    day_trip_draft.clear()
    trip_fees.clear()

    if plan is not None:
        for day in plan.get_days():
            if day != None:
                day = Day.query.filter_by(id=day).first()
                destination = Destination.query.filter_by(id=day.destination_id).first()
                attraction = Target.query.filter_by(id=day.attraction_id).first()
                accommodation = Target.query.filter_by(id=day.accommodation_id).first()
                traffic = Target.query.filter_by(id=day.traffic_id).first()
                day = [len(day_trip_draft) + 1, destination.name, attraction.name, accommodation.name, traffic.name]
                day_trip_draft.append(day)
                trip_fees.append(attraction.price)
                trip_fees.append(accommodation.price)
                trip_fees.append(traffic.price)
    return "success"


@staff_blueprint.route('/staff/view_plan/<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/view_plan', methods=['GET', 'POST'])
def view_plan(plan_id=None):
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))

    plan_form = PlanForm()
    day_form = DayTripForm()

    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    total = 0
    for fee in trip_fees:
        total += fee

    if plan_id is None or plan_id == "null":
        return render_template('./staff_site/new_plan.html', days=day_trip_draft, fees=total,
                           plan_form=plan_form, day_form=day_form, destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, user=current_user)
    else:
        plan = db.session.query(Combination).filter_by(id=plan_id).first()
        return render_template('./staff_site/plan_detail.html', plan=plan, days=day_trip_draft, fees=total,
                           plan_form=plan_form, day_form=day_form, destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, user=current_user)


@staff_blueprint.route('/staff/contents/add/<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/contents/add', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/contents/add/', methods=['GET', 'POST'])
def add_new_day(plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
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

            trip_fees.append(attraction.price)
            trip_fees.append(accommodation.price)
            trip_fees.append(traffic.price)

    return redirect(url_for("staff_site.view_plan", plan_id=plan_id))


@staff_blueprint.route('/staff/move_early/<index>,<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/move_early/<index>', methods=['GET', 'POST'])
def move_early(index, plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    index = int(index)
    if index > 0:
        # move fees positions in trip_fees, skip the first one, which is the total price
        trip_fees.insert((index - 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index - 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index - 1) * 3, trip_fees.pop(index * 3))
        # move day trip positions in day_trip_draft
        day_trip_draft.insert(index - 1, day_trip_draft.pop(index))
        for i in range(index - 1, day_trip_draft.__len__()):
            day_trip_draft[i][0] = i + 1
    return redirect(url_for("staff_site.view_plan", plan_id=plan_id))


@staff_blueprint.route('/staff/move_later/<index>,<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/move_later/<index>', methods=['GET', 'POST'])
def move_later(index, plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    index = int(index)
    if index < day_trip_draft.__len__() - 1:
        # move fees positions in trip_fees, skip the first one, which is the total price
        trip_fees.insert((index + 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index + 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index + 1) * 3, trip_fees.pop(index * 3))
        # move day trip positions in day_trip_draft
        day_trip_draft.insert(index + 1, day_trip_draft.pop(index))
        for i in range(index, day_trip_draft.__len__()):
            day_trip_draft[i][0] = i + 1
    return redirect(url_for("staff_site.view_plan", plan_id=plan_id))


@staff_blueprint.route('/staff/delete_day/<index>, <plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/delete_day/<index>', methods=['GET', 'POST'])
def delete_day(index, plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    index = int(index)
    day_trip_draft.pop(index)
    for i in range(index, day_trip_draft.__len__()):
        day_trip_draft[i][0] = i + 1
    trip_fees.pop(index * 3)
    trip_fees.pop(index * 3)
    trip_fees.pop(index * 3)
    return redirect(url_for("staff_site.view_plan", plan_id=plan_id))


@staff_blueprint.route('/staff/contents/update_plan/<plan_id>', methods=['GET', 'POST'])
def update_plan(plan_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plan = Combination.query.filter_by(id=plan_id).first()

    for day in plan.get_days():
        day = Day.query.filter_by(id=day).first()
        if day is not None:
            db.session.delete(day)
            db.session.commit()

    plan.price = 0

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

    # self, name, intro, price, length, day1, day2, day3, day4, day5, day6, day7
    plan.name = name
    plan.intro = intro
    plan.price = price
    plan.length = length
    plan.path = path
    plan.day1 = days_id[0]
    plan.day2 = days_id[1]
    plan.day3 = days_id[2]
    plan.day4 = days_id[3]
    plan.day5 = days_id[4]
    plan.day6 = days_id[5]
    plan.day7 = days_id[6]
    db.session.commit()

    return redirect(url_for("staff_site.contents", message="Update successfully!"))


@staff_blueprint.route('/staff/contents/submit_plan', methods=['GET', 'POST'])
def submit_plan():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
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
    return redirect(url_for("staff_site.contents", message="Submit successfully!"))


@staff_blueprint.route('/staff/contents/clear', methods=['GET', 'POST'])
def clear_draft():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    day_trip_draft.clear()
    trip_fees.clear()
    return redirect(url_for("staff_site.view_plan"))


@staff_blueprint.route('/staff/delete_plan/<plan_id>', methods=['GET', 'POST'])
def delete_plan(plan_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    plan = Combination.query.filter_by(id=plan_id).first()

    day_ids = plan.get_days()
    for day_id in day_ids:
        delete_day_relate(day_id)

    db.session.commit()
    return redirect(url_for("staff_site.contents", message="Delete successfully!"))


@staff_blueprint.route('/staff/contents/destinations', methods=['GET', 'POST'])
def destinations():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
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
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
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
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
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
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
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
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    des_id = int(session.get('des_id'))
    destination = Destination.query.filter_by(id=des_id).first()
    db.session.delete(destination)
    for day in Day.query.filter_by(destination_id=des_id).all():
        delete_day_relate(day.id)

    db.session.commit()
    return redirect(url_for("staff_site.destinations", message="Delete successfully!"))


@staff_blueprint.route('/staff/contents/attractions/delete', methods=['GET', 'POST'])
def delete_attraction():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    attr_id = int(session.get('attr_id'))
    attraction = Target.query.filter_by(id=attr_id).first()
    db.session.delete(attraction)
    for day in Day.query.filter_by(attraction_id=attr_id).all():
        delete_day_relate(day.id)

    db.session.commit()
    return redirect(url_for("staff_site.attractions", message="Delete successfully!"))
    # return redirect(url_for("staff_site.attractions", message="Delete successfully!"))


@staff_blueprint.route('/staff/contents/accommodations/delete', methods=['GET', 'POST'])
def delete_accommodation():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    acc_id = int(session.get('acc_id'))
    accommodation = Target.query.filter_by(id=acc_id).first()
    db.session.delete(accommodation)
    for day in Day.query.filter_by(accommodation_id=acc_id).all():
        delete_day_relate(day.id)
    db.session.commit()
    return redirect(url_for("staff_site.accommodations", message="Delete successfully!"))


@staff_blueprint.route('/staff/contents/traffics/delete', methods=['GET', 'POST'])
def delete_traffic():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    traffic_id = int(session.get('tra_id'))
    traffic = Target.query.filter_by(id=traffic_id).first()
    db.session.delete(traffic)
    for day in Day.query.filter_by(traffic_id=traffic_id).all():
        delete_day_relate(day.id)
    db.session.commit()
    return redirect(url_for("staff_site.traffics", message="Delete successfully!"))


@login_manager.user_loader
def load_user(id):
    return User.get(int(id))


@staff_blueprint.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
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

    u.avatar_url = path
    u.gender = gender
    u.birthday = birth
    u.profession = profession
    u.address = address
    db.session.commit()
    return redirect(url_for('profile'))


@staff_blueprint.route('/staff/pack_orders', methods=['GET', 'POST'])
def pack_orders():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    records = RecordC.query.all()
    return render_template('./staff_site/pack_orders.html', records=records, user=current_user, message="")


@staff_blueprint.route('/staff/other_orders', methods=['GET', 'POST'])
def other_orders():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    records = Record.query.all()
    return render_template('./staff_site/pack_orders.html', records=records, user=current_user, message="")


@staff_blueprint.route('/staff/pack_order/delete', methods=['GET', 'POST'])
def delete_pack_order():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    pack_order_id = int(session.get('pack_order_id'))
    pack_order = RecordC.query.filter_by(id=pack_order_id).first()
    db.session.delete(pack_order)
    db.session.commit()
    return redirect(url_for("staff_site.pack_orders", message="Delete successfully!"))


@staff_blueprint.route('/staff/other_order/delete', methods=['GET', 'POST'])
def delete_other_order():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    other_order_id = int(session.get('other_order_id'))
    other_order = Record.query.filter_by(id=other_order_id).first()
    db.session.delete(other_order)
    db.session.commit()
    return redirect(url_for("staff_site.other_orders", message="Delete successfully!"))


@staff_blueprint.route('/check_message', methods=['GET', 'POST'])
def check_message():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    messages = db.session.query(ContactModel).all()
    contents = []
    names = []
    emails = []
    times = []
    ids = []
    for message in messages:
        c = message.message
        co = c[:9]
        if len(c) <= 10:
            content = c
        else:
            content = co + "......"
        contents.append(content)
        name = message.name
        names.append(name)
        email = message.email
        emails.append(email)
        time = message.create_time
        times.append(time)
        id = message.id
        ids.append(id)
    return render_template('./staff_site/message.html', user=current_user, contents=contents,
                           names=names, emails=emails, times=times, ids=ids)


@staff_blueprint.route('/check_message_details/<message_id>', methods=['GET', 'POST'])
def check_message_details(message_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    message = db.session.query(ContactModel).filter_by(id=message_id).first()
    return render_template('./staff_site/message_detail.html', message=message, user=current_user)


@staff_blueprint.route('/staff/customised_packages', methods=['GET', 'POST'])
def customised_packages():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plans = db.session.query(UserCombination).all()
    return render_template('./staff_site/customised_packages.html', plans=plans, user=current_user)


@staff_blueprint.route('/staff/delete_customised/<plan_id>', methods=['GET', 'POST'])
def delete_customised(plan_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plan = db.session.query(UserCombination).filter_by(id=plan_id).first()
    day_ids = plan.get_days()
    for day_id in day_ids:
        delete_day_relate(day_id)
    db.session.delete(plan)
    db.session.commit()
    return redirect(url_for("staff_site.customised_packages", message="Delete successfully!"))


@staff_blueprint.route('/staff/load_detail', methods=['GET', 'POST'])
def load_detail():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plan_id_res = request.args.get("plan_id_res")

    plan = db.session.query(UserCombination).filter_by(id=plan_id_res).first()
    customised_day_trip_draft.clear()
    customised_trip_fees.clear()

    if plan is not None:
        for day_id in plan.get_days():
            day = Day.query.filter_by(id=day_id).first()
            if day != None:
                destination = Destination.query.filter_by(id=day.destination_id).first()
                attraction = Target.query.filter_by(id=day.attraction_id).first()
                accommodation = Target.query.filter_by(id=day.accommodation_id).first()
                traffic = Target.query.filter_by(id=day.traffic_id).first()
                day = [len(customised_day_trip_draft) + 1, destination.name, attraction.name, accommodation.name, traffic.name]
                customised_day_trip_draft.append(day)
                customised_trip_fees.append(attraction.price)
                customised_trip_fees.append(accommodation.price)
                customised_trip_fees.append(traffic.price)
    return "success"


# @staff_blueprint.route('/staff/customised_detail/<plan_id>/<data>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_detail/<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_detail', methods=['GET', 'POST'])
def customised_detail(plan_id=None, data=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))

    plan_form = PlanForm()
    day_form = DayTripForm()

    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    total = 0
    for fee in customised_trip_fees:
        total += fee

    if plan_id is None or plan_id == "null":
        return render_template('./staff_site/new_customised.html', data=data, days=customised_day_trip_draft, fees=total,
                           plan_form=plan_form, day_form=day_form, destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, user=current_user)
    else:
        plan = db.session.query(UserCombination).filter_by(id=plan_id).first()
        return render_template('./staff_site/customised_detail.html', data=data, plan=plan, days=customised_day_trip_draft, fees=total,
                           plan_form=plan_form, day_form=day_form, destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, user=current_user)


@staff_blueprint.route('/staff/customised_add_new_day/<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_add_new_day', methods=['GET', 'POST'])
def customised_add_new_day(plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    # changeBookingStatus()
    form = DayTripForm(request.form)
    if form.validate_on_submit() and customised_day_trip_draft.__len__() < 7:
        destination = form.destination.data
        attraction = form.attraction.data
        accommodation = form.accommodation.data
        traffic = form.traffic.data
        customised_day_trip_draft.append([len(customised_day_trip_draft) + 1,
                                          destination, attraction, accommodation, traffic])

        attraction = Target.query.filter_by(name=attraction).first()
        accommodation = Target.query.filter_by(name=accommodation).first()
        traffic = Target.query.filter_by(name=traffic).first()

        customised_trip_fees.append(attraction.price)
        customised_trip_fees.append(accommodation.price)
        customised_trip_fees.append(traffic.price)

    return redirect(url_for("staff_site.customised_detail", plan_id=plan_id))


@staff_blueprint.route('/staff/customised_move_early/<index>,<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_move_early/<index>', methods=['GET', 'POST'])
def customised_move_early(index, plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    index = int(index)
    if index > 0:
        # move fees positions in customised_trip_fees, skip the first one, which is the total price
        customised_trip_fees.insert((index - 1) * 3, customised_trip_fees.pop(index * 3))
        customised_trip_fees.insert((index - 1) * 3, customised_trip_fees.pop(index * 3))
        customised_trip_fees.insert((index - 1) * 3, customised_trip_fees.pop(index * 3))
        # move day trip positions in customised_day_trip_draft
        customised_day_trip_draft.insert(index - 1, customised_day_trip_draft.pop(index))
        for i in range(index - 1, customised_day_trip_draft.__len__()):
            customised_day_trip_draft[i][0] = i + 1
    return redirect(url_for("staff_site.customised_detail", plan_id=plan_id))


@staff_blueprint.route('/staff/customised_move_later/<index>,<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_move_later/<index>', methods=['GET', 'POST'])
def customised_move_later(index, plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    index = int(index)
    if index < customised_day_trip_draft.__len__() - 1:
        # move fees positions in customised_trip_fees, skip the first one, which is the total price
        customised_trip_fees.insert((index + 1) * 3, customised_trip_fees.pop(index * 3))
        customised_trip_fees.insert((index + 1) * 3, customised_trip_fees.pop(index * 3))
        customised_trip_fees.insert((index + 1) * 3, customised_trip_fees.pop(index * 3))
        # move day trip positions in customised_day_trip_draft
        customised_day_trip_draft.insert(index + 1, customised_day_trip_draft.pop(index))
        for i in range(index, customised_day_trip_draft.__len__()):
            customised_day_trip_draft[i][0] = i + 1
    return redirect(url_for("staff_site.customised_detail", plan_id=plan_id))


@staff_blueprint.route('/staff/customised_delete_day/<index>, <plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_delete_day/<index>', methods=['GET', 'POST'])
def customised_delete_day(index, plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    index = int(index)
    customised_day_trip_draft.pop(index)
    for i in range(index, customised_day_trip_draft.__len__()):
        customised_day_trip_draft[i][0] = i + 1
    customised_trip_fees.pop(index * 3)
    customised_trip_fees.pop(index * 3)
    customised_trip_fees.pop(index * 3)
    return redirect(url_for("staff_site.customised_detail", plan_id=plan_id))


@staff_blueprint.route('/staff/contents/customised_update_plan/<plan_id>', methods=['GET', 'POST'])
def customised_update_plan(plan_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    plan = UserCombination.query.filter_by(id=plan_id).first()

    for day in plan.get_days():
        day = Day.query.filter_by(id=day).first()
        if day is not None:
            db.session.delete(day)
            db.session.commit()

    plan.price = 0

    user_id = request.form.get('user_id')
    name = request.form.get('name')
    intro = request.form.get('intro')
    price = request.form.get('price')
    length = customised_day_trip_draft.__len__()
    days = []

    for day in customised_day_trip_draft:
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

    # self, user_id, name, intro, price, length, day1, day2, day3, day4, day5, day6, day7
    plan.user_id = user_id
    plan.name = name
    plan.intro = intro
    plan.price = price
    plan.length = length
    plan.day1 = days_id[0]
    plan.day2 = days_id[1]
    plan.day3 = days_id[2]
    plan.day4 = days_id[3]
    plan.day5 = days_id[4]
    plan.day6 = days_id[5]
    plan.day7 = days_id[6]
    db.session.commit()

    return redirect(url_for("staff_site.customised_packages", message="Update successfully!"))


@staff_blueprint.route('/staff/customised_update_clear_draft/<plan_id>', methods=['GET', 'POST'])
@staff_blueprint.route('/staff/customised_update_clear_draft', methods=['GET', 'POST'])
def customised_clear_draft(plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    customised_day_trip_draft.clear()
    customised_trip_fees.clear()
    return redirect(url_for("staff_site.customised_detail", plan_id=plan_id))


@staff_blueprint.route('/staff/contents/customised_submit_plan', methods=['GET', 'POST'])
def customised_submit_plan():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    # changeBookingStatus()
    user_id = request.form.get('user_id')
    name = request.form.get('name')
    intro = request.form.get('intro')
    price = request.form.get('price')
    length = customised_day_trip_draft.__len__()
    days = []


    for day in customised_day_trip_draft:
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

    # self, user_id, name, intro, price, length, day1, day2, day3, day4, day5, day6, day7
    combination = UserCombination(user_id, name, intro, price, length, days_id[0], days_id[1], days_id[2], days_id[3],
                              days_id[4], days_id[5], days_id[6])
    db.session.add(combination)
    db.session.commit()
    customised_day_trip_draft.clear()
    return redirect(url_for("staff_site.customised_packages", message="Submit successfully!"))


@staff_blueprint.route('/staff/clear_res', methods=['GET', 'POST'])
def clear_res():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    customised_day_trip_draft.clear()
    customised_trip_fees.clear()
    return "success"


@staff_blueprint.route('/staff/customised_delete_plan/<plan_id>', methods=['GET', 'POST'])
def customised_delete_plan(plan_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    # changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    plan = UserCombination.query.filter_by(id=plan_id).first()

    day_ids = plan.get_days()
    for day_id in day_ids:
        delete_day_relate(day_id)
    db.session.delete(plan)
    db.session.commit()
    return redirect(url_for("staff_site.customised_packages", message="Delete successfully!"))


@staff_blueprint.route('/staff/customer_accounts', methods=['GET', 'POST'])
def customer_accounts():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    users = User.query.filter_by(is_admin=0).all()
    return render_template("./staff_site/customers.html", users=users, user=current_user)


@staff_blueprint.route('/staff/staff_accounts', methods=['GET', 'POST'])
def staff_accounts():
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    users = User.query.filter_by(is_admin=1).all()
    return render_template("./staff_site/staffs.html", users=users, user=current_user)


@staff_blueprint.route('/staff/delete_user/<id>', methods=['GET', 'POST'])
def delete_user(id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    user = User.query.filter_by(id=id).first()
    if user is not None:
        for record in Record.query.filter_by(user_id=id).all():
            db.session.delete(record)
        for record in RecordC.query.filter_by(user_id=id).all():
            db.session.delete(record)
        for record in RecordP.query.filter_by(user_id=id).all():
            db.session.delete(record)
        for comment in Comment.query.filter_by(user_id=id).all():
            db.session.delete(comment)
        for comment in CommentC.query.filter_by(user_id=id).all():
            db.session.delete(comment)
        for favorite in Favorite.query.filter_by(user_id=id).all():
            db.session.delete(favorite)
        for favorite in FavoriteC.query.filter_by(user_id=id).all():
            db.session.delete(favorite)
        for combination in UserCombination.query.filter_by(user_id=id).all():
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("staff_site.customer_accounts"))

def delete_combination_relate(combination_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    for record in RecordC.query.filter_by(combination_id=combination_id).all():
        db.session.delete(record)
    for comment in CommentC.query.filter_by(combination_id=combination_id).all():
        db.session.delete(comment)
    for favorite in FavoriteC.query.filter_by(combination_id=combination_id).all():
        db.session.delete(favorite)
    db.session.commit()


def delete_day_relate(day_id):
    if not current_user.is_authenticated:
        return redirect(url_for("staff_site.login"))
    if not current_user.is_admin == 1:
        return redirect(url_for("staff_site.login"))
    day = Day.query.filter_by(id=day_id).first()
    if day is not None:
        db.session.delete(day)

    for combination in Combination.query.all():
        if combination.day1 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        elif combination.day2 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        elif combination.day3 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        elif combination.day4 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        elif combination.day5 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        elif combination.day6 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)
        elif combination.day7 == day_id:
            delete_combination_relate(combination.id)
            db.session.delete(combination)

    for combination in UserCombination.query.all():
        # print("ok", day_id)
        # print(combination.day1, combination.day2, combination.day3, combination.day4, combination.day5, combination.day6, combination.day7)
        if combination.day1 == day_id:
            for record in RecordP.query.filter_by(combination_id=combination.id).all():
                db.session.delete(record)
            db.session.delete(combination)
        elif combination.day2 == day_id:
            for record in RecordP.query.filter_by(combination_id=combination.id).all():
                db.session.delete(record)
            db.session.delete(combination)
        elif combination.day3 == day_id:
            for record in RecordP.query.filter_by(combination_id=combination.id).all():
                db.session.delete(record)
            db.session.delete(combination)
        elif combination.day4 == day_id:
            for record in RecordP.query.filter_by(combination_id=combination.id).all():
                db.session.delete(record)
            db.session.delete(combination)
        elif combination.day5 == day_id:
            db.session.delete(combination)
        elif combination.day6 == day_id:
            for record in RecordP.query.filter_by(combination_id=combination.id).all():
                db.session.delete(record)
            db.session.delete(combination)
        elif combination.day7 == day_id:
            for record in RecordP.query.filter_by(combination_id=combination.id).all():
                db.session.delete(record)
            db.session.delete(combination)
    db.session.commit()

