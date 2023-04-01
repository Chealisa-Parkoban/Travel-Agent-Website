from datetime import time

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from travelAgent import db
from travelAgent import app
from travelAgent.models import Combination, RecordC
from travelAgent.forms import BookingForm

booking_blueprint = Blueprint(name="booking", import_name=__name__)

booking_blueprint.route('/', methods=['GET', 'POST'])


def addBooking():
    form = BookingForm(request.form)
    if request.method == 'GET':
        bookings = RecordC.query.all()
        return render_template('/', bookings=bookings, form=form)
    else:
        if form.validate_on_submit():
            start_time = form.time.data
            num = form.num.data
            name = form.name.data
            tel = form.tel.data

            booking = RecordC(user_id=current_user.id, combination_id=1, start_time=start_time, num=num,
                              name=name, tel=tel, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            db.session.add(booking)
            return redirect(url_for('/'))

