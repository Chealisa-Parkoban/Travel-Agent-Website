import time

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user

from travelAgent import db
from travelAgent import app
from travelAgent.models import Combination, RecordC
from travelAgent.forms import BookingForm

booking_blueprint = Blueprint(name="booking", import_name=__name__)


@booking_blueprint.route('/booking/<combination_id>', methods=['GET', 'POST'])
def addBooking(combination_id):
    form = BookingForm(request.form)
    if request.method == 'GET':
        # bookings = RecordC.query.all()
        # print("Ssdssssssssssss")
        return render_template('book.html', form=form, combination_id=combination_id)
    else:
        if form.validate_on_submit():
            start_time = form.time.data
            num = form.num.data
            name = form.name.data
            tel = form.tel.data
            booking = RecordC(user_id=current_user.id, combination_id=combination_id, start_time=start_time, num=num,
                              name=name, tel=tel, time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            db.session.add(booking)
            db.session.commit()
            # print("ffffffffffffffffff")
            return redirect(url_for("booking.addBooking", combination_id=combination_id))
        else:
            # print("hhhhhhhhhhhh")
            return render_template('book.html', combination_id=combination_id)


@booking_blueprint.route('/deleteBooking/<booking_id>', methods=['GET', 'POST'])
def deleteBooking(booking_id):
    # db.session.query(RecordC).filter(RecordC.id == booking_id).delete()
    booking = RecordC.query.filter_by(id=booking_id).first()
    db.session.delete(booking)
    db.session.commit()
    return render_template('profile.html')

@booking_blueprint.route('/changeBooking/<booking_id>', methods=['GET', 'POST'])
def changeBooking(booking_id):
    form = BookingForm(request.form)
    if request.method == 'GET':
        # bookings = RecordC.query.all()
        # print("Ssdssssssssssss")
        return render_template('profile.html', form=form, booking_id=booking_id)
    else:
        if form.validate_on_submit():
            start_time = form.time.data
            num = form.num.data
            name = form.name.data
            tel = form.tel.data
            RecordC.query.filter_by(id=booking_id).update({'start_time': start_time, 'num': num, 'name': name, 'tel': tel })
            db.session.commit()
            # print("ffffffffffffffffff")
            return render_template('profile.html')
        else:
            # print("hhhhhhhhhhhh")
            return render_template('profile.html')








