import datetime
import time

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user

from travelAgent import db
from travelAgent import app
from travelAgent.models import Combination, RecordC, Target, Record, UserCombination, RecordP
from travelAgent.forms import BookingForm, BookingHotelForm

booking_blueprint = Blueprint(name="booking", import_name=__name__)


@booking_blueprint.route('/booking/<combination_id>', methods=['GET', 'POST'])
def addBooking(combination_id):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))
    combination = Combination.query.filter_by(id=combination_id).first()
    form = BookingForm(request.form)
    if request.method == 'GET':
        # bookings = RecordC.query.all()
        # print("Ssdssssssssssss")
        return render_template('book.html', form=form, combination_id=combination_id, combination=combination)
    else:

        if form.validate_on_submit():
            start_time = form.time.data
            num = int(form.num.data)
            name = form.name.data
            tel = form.tel.data
            unit_price=int(combination.price)
            total_price=unit_price*num
            booking = RecordC(user_id=current_user.id, combination_id=combination_id, start_time=start_time, num=num,
                              name=name, tel=tel, time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), price=total_price, status="Uncompleted", status2="No comment")

            if len(tel) == 11:
                db.session.add(booking)
                db.session.commit()
                return redirect("/order_list")

            else:
                flash("Wrong phone number, please enter a phone number consisting of 11 digits only")
                return render_template('book.html', form=form, combination_id=combination_id, combination=combination)
        else:
            return render_template('book.html', combination_id=combination_id, combination=combination)


@booking_blueprint.route('/booking_another/<target_id>', methods=['GET', 'POST'])
def addTargetBooking(target_id):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))
    target = Target.query.filter_by(id=target_id).first()
    target_type = target.type
    if target_type == 0:
        form = BookingForm(request.form)
    else:
        form = BookingHotelForm(request.form)
    if request.method == 'GET':
        if target_type == 0:
            return render_template('book_attraction.html', form=form, target_id=target_id, target=target)
        elif target_type == 1:
            return render_template('book_hotel.html', form=form, target_id=target_id, target=target)

    else:

        if form.validate_on_submit():
            start_time = form.time.data
            num = int(form.num.data)
            name = form.name.data
            tel = form.tel.data
            unit_price=int(target.price)
            total_price=unit_price*num
            if target_type == 0:
                booking = Record(user_id=current_user.id, target_id=target_id, start_time=start_time, end_time=start_time, num=num,
                              name=name, tel=tel, time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), price=total_price, status="Uncompleted", status2="No comment")
            elif target_type == 1:
                end_time = form.time2.data
                time1 = datetime.datetime.strptime(start_time,'%Y-%m-%d')
                time2 = datetime.datetime.strptime(end_time,'%Y-%m-%d')
                duration = time2 - time1
                total_price = total_price * duration.days
                booking = Record(user_id=current_user.id, target_id=target_id, start_time=start_time, end_time=end_time, num=num,
                                 name=name, tel=tel, time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                                 price=total_price, status="Uncompleted", status2="No comment")

            if booking.price > 0 and len(tel) == 11:
                db.session.add(booking)
                db.session.commit()
                return redirect("/order_list")
            elif booking.price <= 0:
                flash("The date you selected is incorrect Please fill in again")
                return render_template('book_hotel.html', form=form, target_id=target_id, target=target)
            elif len(tel) != 11:
                flash("Wrong phone number, please enter a phone number consisting of 11 digits only")
                if target_type == 0:
                    return render_template('book_attraction.html', form=form, target_id=target_id, target=target)
                elif target_type == 1:
                    return render_template('book_hotel.html', form=form, target_id=target_id, target=target)

        else:
            if target_type == 0:
                return render_template('book_attraction.html', form=form, target_id=target_id, target=target)
            elif target_type == 1:
                return render_template('book_hotel.html', form=form, target_id=target_id, target=target)


@booking_blueprint.route('/personal_booking/<combination_id>', methods=['GET', 'POST'])
def addPersonalBooking(combination_id):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))
    combination = UserCombination.query.filter_by(id=combination_id).first()
    form = BookingForm(request.form)
    if request.method == 'GET':
        return render_template('book_personal.html', form=form, combination_id=combination_id, combination=combination)
    else:
        if form.validate_on_submit():
            start_time = form.time.data
            num = int(form.num.data)
            name = form.name.data
            tel = form.tel.data
            unit_price=int(combination.price)
            total_price=unit_price*num
            booking = RecordP(user_id=current_user.id, combination_id=combination_id, start_time=start_time, num=num,
                              name=name, tel=tel, time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), price=total_price, status="Uncompleted", status2="No comment")
            db.session.add(booking)
            db.session.commit()
            if len(tel) == 11:
                db.session.add(booking)
                db.session.commit()
                return redirect("/order_list")
            else:
                flash("Wrong phone number, please enter a phone number consisting of 11 digits only")
                return render_template('book.html', form=form, combination_id=combination_id, combination=combination)

        else:
            return render_template('book_personal.html', combination_id=combination_id, combination=combination)


@booking_blueprint.route('/deleteBooking/<booking_id>', methods=['GET', 'POST'])
def deleteBooking(booking_id):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))
    # db.session.query(RecordC).filter(RecordC.id == booking_id).delete()
    booking = RecordC.query.filter_by(id=booking_id).first()
    db.session.delete(booking)
    db.session.commit()
    return render_template('profile.html')


@booking_blueprint.route('/changeBooking/<booking_id>', methods=['GET', 'POST'])
def changeBooking(booking_id):
    if not current_user.is_authenticated:
        return redirect(url_for("account.login"))
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


















