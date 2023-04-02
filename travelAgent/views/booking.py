from datetime import time

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from travelAgent import db
from travelAgent import app
from travelAgent.models import Combination, RecordC
from travelAgent.forms import BookingForm

booking_blueprint = Blueprint(name="booking", import_name=__name__)


@booking_blueprint.route('/booking', methods=['GET', 'POST'])
def addBooking():
    form = BookingForm(request.form)
    if request.method == 'GET':
        # bookings = RecordC.query.all()
        # print("Ssdssssssssssss")
        return render_template('book.html', form=form)
    else:
        if form.validate_on_submit():
            start_time = form.time.data
            num = form.num.data
            name = form.name.data
            tel = form.tel.data
            booking = RecordC(user_id=current_user.id, combination_id=1, start_time=start_time, num=num,
                              name=name, tel=tel, time=start_time)
            db.session.add(booking)
            db.session.commit()
            # print("ffffffffffffffffff")
            return redirect(url_for("booking.addBooking"))
        else:
            # print("hhhhhhhhhhhh")
            return render_template('book.html')

