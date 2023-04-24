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


@planning_tool_blueprint.route('/planning', methods=['GET', 'POST'])
def planning(save_draft=False):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))


    if not save_draft:
        day_trip_draft.clear()
        trip_fees.clear()

    day_form = DayTripForm(request.form)
    plan_form = PlanForm(request.form)
    destinations = Destination.query.all()
    attractions = Target.query.filter_by(type="0").all()
    accommodations = Target.query.filter_by(type="1").all()
    traffics = Target.query.filter_by(type="2").all()

    fees = 0
    for fee in trip_fees:
        fees += fee
    return render_template('planning_tool.html', day_form=day_form, plan_form=plan_form, days=day_trip_draft,
                           destinations=destinations, attractions=attractions,
                           accommodations=accommodations, traffics=traffics, trip_fees=fees, user=current_user)


@planning_tool_blueprint.route('/planning/add', methods=['GET', 'POST'])
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

            attraction = Target.query.filter_by(name=attraction).first()
            accommodation = Target.query.filter_by(name=accommodation).first()
            traffic = Target.query.filter_by(name=traffic).first()

            trip_fees.append(attraction.price)
            trip_fees.append(accommodation.price)
            trip_fees.append(traffic.price)

    # save_draft[0] = True
    # return redirect(url_for("planning_tool.planning)"))
    return planning(True)


@planning_tool_blueprint.route('/planning/get_day_num', methods=['GET', 'POST'])
def get_day_num():
    return str(day_trip_draft.__len__())


@planning_tool_blueprint.route('/planning/clear', methods=['GET', 'POST'])
def clear_draft():
    day_trip_draft.clear()
    return redirect(url_for("planning_tool.planning"))


@planning_tool_blueprint.route('/planning/submit_plan', methods=['GET', 'POST'])
def submit_plan():
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

    if not current_user.is_authenticated:
        user_id = 0
    else:
        user_id = current_user.id

    combination = UserCombination(name, user_id, intro, price, length, days_id[0], days_id[1], days_id[2], days_id[3],
                              days_id[4], days_id[5], days_id[6])
    db.session.add(combination)
    db.session.commit()
    day_trip_draft.clear()
    return redirect(url_for("planning_tool.planning"))





