import datetime
import time

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user

from travelAgent import db
from travelAgent import app
from travelAgent.models import Combination, RecordC, Target, Record, UserCombination, RecordP, FavoriteC
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


def popular(sets, records, id_type):
    dic = {}
    # default: every combination in db has a value 1
    for s in sets:
        dic[s.id] = 0

    # print("basic-----------------")
    # print(dic)
    # print("records-----------")
    # print(records)

    # increase value according to the record table
    # id_type = 0 :combination /
    # 1:target
    if id_type == 0:
        for r in records:
            temp = dic[r.combination_id]
            dic[r.combination_id] = temp + 1
    else:
        for r in records:
            # key = r.target_id
            # check if id exists in original dic( as different types
            if r.target_id in dic.keys():
                temp = dic[r.target_id]
                dic[r.target_id] = temp + 1
    # print("update-----------------")
    # print(dic)

    e = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    return e

def sorted_set(lst, id_type):
    real_sets = []
    #
    if id_type == 0:
        for unit in lst:
            combination = Combination.query.filter(Combination.id == unit[0]).first()
            real_sets.append(combination)

    else:
        for unit in lst:
            target = Target.query.filter(Target.id == unit[0]).first()
            real_sets.append(target)

    return real_sets


def update_num(lst, id_type, num_type):
    #
    if id_type == 0:
        for unit in lst:
            combination = Combination.query.filter(Combination.id == unit[0]).first()
            if num_type == 0:
                combination.num_orders = unit[1]
            else:
                combination.num_favorite = unit[1]
            db.session.commit()

    else:
        for unit in lst:
            target = Target.query.filter(Target.id == unit[0]).first()
            if num_type == 0:
                target.num_orders = unit[1]
            else:
                target.num_favorite = unit[1]
            db.session.commit()

def update_score(sets, comments, id_type):
    dic = {}
    # default: every element in db no scores
    for s in sets:
        # multi dic [0]:the count [1]: the total value
        dic.setdefault(s.id, []).append(0)
        dic.setdefault(s.id, []).append('No score')

    # increase value according to the comment table
    # id_type = 0 :combination /
    # 1:target
    if id_type == 0:
        for r in comments:
            # print("Start------------comment combination id: ",r.combination_id)
            # print("count: ", dic[r.combination_id][0])
            # print("total", dic[r.combination_id][1])
            dic[r.combination_id][0] = dic[r.combination_id][0] + 1
            if dic[r.combination_id][0] == 1:
                dic[r.combination_id][1] = r.score
            else:
                dic[r.combination_id][1] = r.score + dic[r.combination_id][1]
            # print("after----------------", r.combination_id)
            # print("count: ", dic[r.combination_id][0])
            # print("total", dic[r.combination_id][1])
    else:
        for r in comments:
            if r.target_id in dic.keys():
                dic[r.target_id][0] = dic[r.target_id][0] + 1
                if dic[r.target_id][0] == 1:
                    dic[r.target_id][1] = r.score
                else:
                    dic[r.target_id][1] = r.score + dic[r.target_id][1]


    if id_type == 0:
        for c_id in dic.keys():
            combination = Combination.query.filter(Combination.id == c_id).first()
            if dic[c_id][0] != 0 and type(dic[c_id][0]) is not str:
                avg = dic[c_id][1]/dic[c_id][0]
                avg2 = '{:.2f}'.format(avg)
                combination.avg_score = avg2
                db.session.commit()

    else:
        for t_id in dic.keys():
            target = Target.query.filter(Target.id == t_id).first()
            if dic[t_id][0] != 0 and type(dic[t_id][0]) is not str:
                avg = dic[t_id][1]/dic[t_id][0]
                avg2 = '{:.2f}'.format(avg)
                target.avg_score = avg2
                db.session.commit()

# 更新订单、收藏、平均评分
# 订单：完成预定后
# 收藏：添加、取消收藏后
# 评分：添加评论后
def update_total():
    sets1 = Combination.query.all()
    attractions = Target.query.filter(Target.type == '0').all()
    hotels = Target.query.filter(Target.type == '1').all()

    records_c = RecordC.query.all()
    records_t = Record.query.all()
    fav_c = FavoriteC.query.all()
    fav_t = Favorite.query.all()
    comment_c = CommentC.query.all()
    comment_t = Comment.query.all()

    # list containing the num of orders
    l_combination = popular(sets1, records_c, 0)
    l_attraction = popular(attractions, records_t, 1)
    l_hotel = popular(hotels, records_t, 1)

    # list containing the num of favorite
    l_combination2 = popular(sets1, fav_c, 0)
    l_attraction2 = popular(attractions, fav_t, 1)
    l_hotel2 = popular(hotels, fav_t, 1)

    # sorted by order num
    Sets = sorted_set(l_combination, 0)
    sorted_attractions = sorted_set(l_attraction, 1)
    sorted_hotels = sorted_set(l_hotel, 1)

    # update the num of orders and favorites for each item
    update_num(l_combination, 0, 0)
    update_num(l_combination2, 0, 1)
    update_num(l_attraction, 1, 0)
    update_num(l_attraction2, 1, 1)
    update_num(l_hotel, 1, 0)
    update_num(l_hotel2, 1, 1)

    # update average score for each item
    update_score(sets1, comment_c, 0)
    update_score(attractions, comment_t, 1)
    update_score(hotels, comment_t, 1)

















