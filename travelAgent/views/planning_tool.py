import os
import this
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, logout_user

from travelAgent import app, db
from travelAgent.forms import LoginForm, DayTripForm, PlanForm, DestinationForm, TargetForm
from travelAgent.models import User, Destination, Target, Day, Combination, UserCombination
from travelAgent.views.login_handler import login_manager

from travelAgent.config import basedir

planning_tool_blueprint = Blueprint(name="planning_tool", import_name=__name__)

day_trip_draft = []
# save_draft = [False]
trip_fees = []


@planning_tool_blueprint.route('/planning/load_detail', methods=['GET', 'POST'])
def load_detail():
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))
    plan_id_res = request.args.get("plan_id_res")

    plan = db.session.query(UserCombination).filter_by(id=plan_id_res).first()
    day_trip_draft.clear()
    trip_fees.clear()

    if plan is not None:
        for day in plan.get_days():
            if day is not None:
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


@planning_tool_blueprint.route('/planning/<plan_id>', methods=['GET', 'POST'])
@planning_tool_blueprint.route('/planning', methods=['GET', 'POST'])
def planning(plan_id=None):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))

    day_form = DayTripForm(request.form)
    plan_form = PlanForm(request.form)

    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    total = 0
    for fee in trip_fees:
        total += fee

    if plan_id is None or plan_id == "null":
        return render_template('planning_tool.html', day_form=day_form, plan_form=plan_form, days=day_trip_draft,
                           destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, fees=total, user=current_user)
    else:
        plan = db.session.query(UserCombination).filter_by(id=plan_id).first()
        return render_template('personal_plan_detail.html', plan=plan, day_form=day_form, plan_form=plan_form, days=day_trip_draft,
                               destinations=destinations, attractions=attractions,
                               accommodations=accommodations, traffics=traffics, fees=total, user=current_user,
                               plan_id=plan_id)


@planning_tool_blueprint.route('/planning/add_new_day/<plan_id>', methods=['GET', 'POST'])
@planning_tool_blueprint.route('/planning/add_new_day/', methods=['GET', 'POST'])
@planning_tool_blueprint.route('/planning/add_new_day', methods=['GET', 'POST'])
def add_new_day(plan_id=None):
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

    return redirect(url_for('planning_tool.planning', plan_id=plan_id))


@planning_tool_blueprint.route('/planning_move_early/<index>,<plan_id>', methods=['GET', 'POST'])
@planning_tool_blueprint.route('/planning_move_early/<index>', methods=['GET', 'POST'])
def move_early(index, plan_id=None):
    index = int(index)
    if index > 0:
        # move fees positions in trip_fees
        trip_fees.insert((index - 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index - 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index - 1) * 3, trip_fees.pop(index * 3))
        # move day trip positions in day_trip_draft
        day_trip_draft.insert(index - 1, day_trip_draft.pop(index))
        for i in range(index - 1, day_trip_draft.__len__()):
            day_trip_draft[i][0] = i + 1
    return planning(plan_id)


@planning_tool_blueprint.route('/planning_move_later/<index>,<plan_id>', methods=['GET', 'POST'])
@planning_tool_blueprint.route('/planning_move_later/<index>', methods=['GET', 'POST'])
def move_later(index, plan_id=None):
    index = int(index)
    if index < day_trip_draft.__len__() - 1 and index >= 0 and day_trip_draft.__len__() > 1:
        # move fees positions in trip_fees, skip the first one, which is the total price
        trip_fees.insert((index + 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index + 1) * 3, trip_fees.pop(index * 3))
        trip_fees.insert((index + 1) * 3, trip_fees.pop(index * 3))
        # move day trip positions in day_trip_draft
        day_trip_draft.insert(index + 1, day_trip_draft.pop(index))
        for i in range(index, day_trip_draft.__len__()):
            day_trip_draft[i][0] = i + 1
    return planning(plan_id)


@planning_tool_blueprint.route('/planning_delete_day/<index>, <plan_id>', methods=['GET', 'POST'])
@planning_tool_blueprint.route('/planning_delete_day/<index>', methods=['GET', 'POST'])
def delete_day(index, plan_id=None):
    index = int(index)
    if day_trip_draft.__len__() > 1:
        day_trip_draft.pop(index)
    for i in range(index, day_trip_draft.__len__()):
        day_trip_draft[i][0] = i + 1
    if trip_fees.__len__() > 3:
        trip_fees.pop(index * 3)
        trip_fees.pop(index * 3)
        trip_fees.pop(index * 3)
    return planning(plan_id)


@planning_tool_blueprint.route('/planning/update_plan/<plan_id>', methods=['GET', 'POST'])
def update_plan(plan_id):
    plan = UserCombination.query.filter_by(id=plan_id).first()

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
    plan.day1 = days_id[0]
    plan.day2 = days_id[1]
    plan.day3 = days_id[2]
    plan.day4 = days_id[3]
    plan.day5 = days_id[4]
    plan.day6 = days_id[5]
    plan.day7 = days_id[6]
    db.session.commit()

    return redirect(url_for("personal_plan", plan_id=plan_id))


@planning_tool_blueprint.route('/planning/clear', methods=['GET', 'POST'])
def clear_draft():
    day_trip_draft.clear()
    trip_fees.clear()
    return redirect(url_for("planning_tool.planning"))


def submit_plan():
    name = request.form.get('name')
    intro = request.form.get('intro')
    price = request.form.get('price')
    length = day_trip_draft.__len__()
    days = []
    print(name, intro, price, length, day_trip_draft.__len__() )

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

    if not current_user.is_authenticated:
        user_id = 0
    else:
        user_id = current_user.id

    combination = UserCombination(user_id, name, intro, price, length, days_id[0], days_id[1], days_id[2], days_id[3],
                                  days_id[4], days_id[5], days_id[6])
    db.session.add(combination)
    db.session.commit()
    day_trip_draft.clear()
    return combination.id


@planning_tool_blueprint.route('/planning/save_draft', methods=['GET', 'POST'])
def save_draft():
    submit_plan()
    return redirect(url_for("personal_plan"))


@planning_tool_blueprint.route('/planning/buy', methods=['GET', 'POST'])
def buy():
    plan_id = submit_plan()
    return redirect(url_for("booking.addPersonalBooking", combination_id=plan_id))


@planning_tool_blueprint.route('/planning/back', methods=['GET', 'POST'])
def back():
    return redirect(url_for("personal_plan"))


# @planning_tool_blueprint.route('/planning/plan_detail', methods=['GET', 'POST'])
# def plan_detail():
#     plan_id = session['personal_plan_id']
#     plan = UserCombination.query.filter_by(id=plan_id).first()
#     days = []
#     for i in range(1, 8):
#         day = Day.query.filter_by(id=getattr(plan, "day" + str(i))).first()
#         if day is None:
#             continue
#         destination = Destination.query.filter_by(id=day.destination_id).first()
#         attraction = Target.query.filter_by(id=day.attraction_id).first()
#         accommodation = Target.query.filter_by(id=day.accommodation_id).first()
#         traffic = Target.query.filter_by(id=day.traffic_id).first()
#         day = [i, destination.name, attraction.name, accommodation.name, traffic.name]
#         days.append(day)
#     return render_template('personal_plan_detail.html', plan=plan, days=days)





