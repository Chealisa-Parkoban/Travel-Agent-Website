import os
import this
import time

import requests
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import logging
import http.client
import hashlib
import urllib
import random
import json
import datetime
import openai
import base64
# import numpy as np
# import cv2

from datetime import datetime, timedelta
# from aip import AipImageProcess
# aip模块叫做baidu-aip，安装的时候pip install baidu-aip
import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, User, RecordC, UserCombination, \
    Record, RecordP
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, User, RecordC, ContactModel
from flask_mail import Message

from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str
from travelAgent.views.staff_site import staff_blueprint
from travelAgent.views.detail import detail_blueprint, showSetDetails
from travelAgent.views.search import search_blueprint
from travelAgent.views.favorite import favorite_blueprint
from travelAgent.views.booking import booking_blueprint
from travelAgent.views.planning_tool import planning_tool_blueprint
from travelAgent.views.target import target_blueprint
from travelAgent import mail




#<!--------------------chat------------------->
from travelAgent.views.chat import chat_blueprint
from travelAgent.views.chat import socketio, set_logger
app.register_blueprint(chat_blueprint)
#<!--------------------chat------------------->

# -------------------------------------register blueprints------------------------------------------
app.register_blueprint(login_blueprint)
app.register_blueprint(staff_blueprint)
app.register_blueprint(detail_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(favorite_blueprint)
app.register_blueprint(booking_blueprint)
app.register_blueprint(target_blueprint)
app.register_blueprint(planning_tool_blueprint)


# -------------------------------------create a logger------------------------------------------
logger = logging.getLogger(__name__)  # create a logger
logger.setLevel(logging.INFO)  # show messages above info level
basedir = os.path.abspath(os.path.dirname(__file__))  # get the base directory
fh = logging.FileHandler(os.path.join(basedir, 'logs/travelAgent.log'))  # log file handler
ch = logging.StreamHandler()  # input stream handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # set a formatter

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
global setID

@app.route('/')
def index():  # put application's code here
    logger.info('Entered the HOME page')
    changeBookingStatus()
    if current_user.is_authenticated:
        return render_template("index.html", current_user=current_user)
    return render_template("index.html", current_user=None, username=None)


@app.route('/about')
def about():
    logger.info('Entered the ABOUT page')
    changeBookingStatus()
    return render_template("about.html")


@app.route('/contactUs')
def contact_us():
    logger.info('Entered the CONTACT page')
    changeBookingStatus()
    return render_template("contact.html")


def popular(sets, records, id_type):
    dic = {}
    # default: every combination in db has a value 1
    for s in sets:
        dic[s.id] = 1

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
            print(r.target_id)
            # key = r.target_id
            # check if id exists in original dic( as different types
            if r.target_id in dic.keys():
                temp = dic[r.target_id]
                dic[r.target_id] = temp + 1
    # print("update-----------------")
    # print(dic)

    e = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    print(e)
    # e1: sorted keys i.e. combination id
    e1 = []
    for i in e:
        e1.append(i[0])
    # print("id sorted---------------")
    # print(e1)

    real_sets = []
    if id_type == 0:
        for c_id in e1:
            element = Combination.query.filter(Combination.id == c_id).first()
            real_sets.append(element)
    else:
        for t_id in e1:
            element = Target.query.filter(Target.id == t_id).first()
            real_sets.append(element)
    # print("final sets-------------------")
    # print(Sets)
    return real_sets



@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    logger.info('Entered the HOME page')
    changeBookingStatus()
    sets1 = Combination.query.all()
    attractions = Target.query.filter(Target.type == '0').all()
    hotels = Target.query.filter(Target.type == '1').all()

    records_c = RecordC.query.all()
    records_t = Record.query.all()

    Sets = popular(sets1, records_c, 0)
    # attractions = attractions[::-1]
    sorted_attractions = popular(attractions, records_t, 1)
    sorted_hotels = popular(hotels, records_t, 1)
    print("homepage2")
    return render_template("homepage2.html", Sets=Sets, attractions=sorted_attractions, hotels=sorted_hotels)


@app.route('/attractions', methods=['GET', 'POST'])
def attractions():
    changeBookingStatus()
    attractions = Target.query.filter(Target.type == '0').all()
    return render_template("attractions.html", attractions=attractions)


@app.route('/stays', methods=['GET', 'POST'])
def stays():
    changeBookingStatus()
    stays = Target.query.filter(Target.type == '1').all()
    return render_template("stays.html", hotels=stays)

@app.route('/traffics', methods=['GET', 'POST'])
def traffics():
    changeBookingStatus()
    traffics = Target.query.filter(Target.type == '2').all()
    return render_template("traffics.html", traffics=traffics)

@app.route('/personal_plan', methods=['GET', 'POST'])
def personal_plan():
    if current_user.is_authenticated:
        personal_plans = UserCombination.query.filter(UserCombination.user_id == current_user.id).all()
        return render_template("personal_plans.html", plans=personal_plans)
    else:
        return redirect(url_for("account.login"))


# @app.route('/homepage2', methods=['GET', 'POST'])
# def homepage2():
#     logger.info('Entered the HOME page')
#     Sets = Combination.query.all()
#     print("homepage2")
#     return render_template("homepage2.html", Sets=Sets)

@app.route('/book', methods=['GET', 'POST'])
def book():
    changeBookingStatus()
    logger.info('Entered the BOOK page')
    return render_template("book.html")


@app.route('/profile')
def profile():
    changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))
    else:
        customer_id = current_user.id
        # 传递user的个人信息
        user = db.session.query(User).filter(User.id == customer_id).first()
        # 传输个人的booking记录
        book = db.session.query(RecordC).filter(RecordC.user_id == customer_id).first()
        bookings = db.session.query(RecordC).filter(RecordC.user_id == customer_id).all()
        # combination中的信息

        combiantion_name = []
        number = []
        start_time = []
        price = []
        status_complete = []
        status_comment = []


    for book in bookings:
        combination_id = book.combination_id
        print(combination_id)
        combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
        number.append(book.num)
        combiantion_name.append(combination.name)
        start_time.append(book.start_time)
        price.append(book.price)
        status_complete.append(book.status)
        status_comment.append(book.status2)


    return render_template("profile.html", user=user, start_time=start_time, number=number,
                           combiantion_name=combiantion_name, price=price, status=status_complete, status_comment=status_comment)


@app.route('/favourites')
def favourites():
    logger.info('Entered the FAVOURITES page')
    changeBookingStatus()
    return render_template('favourites.html')


@app.route('/order_list')
def order_list():
    logger.info('Entered the order_list page')
    changeBookingStatus()
    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))
    else:
        customer_id = current_user.id
        bookings = db.session.query(RecordC).filter(RecordC.user_id == customer_id).all()

        # combination中的信息
        ids = []
        combination_name = []
        user_name = []
        start_time = []
        number = []
        introduction = []
        tel = []
        image = []
        price = []
        status_complete = []
        status_comment = []

        for book in bookings:
            combination_id = book.combination_id
            print(combination_id)
            combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
            combination_name.append(combination.name)
            user_name.append(book.name)
            number.append(book.num)
            start_time.append(book.start_time)
            tel.append(book.tel)
            introduction.append(combination.intro)
            price.append(book.price)
            image.append(combination.image)
            status_complete.append(book.status)
            status_comment.append(book.status2)
            ids.append(book.id)

        targets = db.session.query(Record).filter(Record.user_id == customer_id).all()
        # targets中的信息
        target_ids = []
        target_user_name = []
        target_name = []
        target_start_time = []
        target_number = []
        target_introduction = []
        target_tel = []
        target_image = []
        target_price = []
        target_status_complete = []
        target_status_comment = []

        for target in targets:
            id = target.target_id
            t = db.session.query(Target).filter(Target.id == id).first()
            target_name.append(t.name)
            target_number.append(target.num)
            target_start_time.append(target.start_time)
            target_tel.append(target.tel)
            target_introduction.append(t.intro)
            target_price.append(target.price)
            target_image.append(t.image)
            target_status_complete.append(target.status)
            target_status_comment.append(target.status2)
            target_ids.append(t.id)
            target_user_name.append(target.name)

        user_combinations = db.session.query(RecordP).filter(RecordP.user_id == customer_id).all()
        # 客制化组合
        user_combination_ids = []
        user_combination_name = []
        user_combination_start_time = []
        user_combination_number = []
        user_combination_introduction = []
        user_combination_tel = []
        user_combination_image = []
        user_combination_price = []
        user_combination_status_complete = []
        user_combination_status_comment = []
        user_combination_user_name = []

        for user_combination in user_combinations:
            combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
            user_combination_name.append(combination.name)
            user_combination_name.append(user_combination.name)
            user_combination_number.append(user_combination.num)
            user_combination_start_time.append(user_combination.start_time)
            user_combination_tel.append(user_combination.tel)
            user_combination_introduction.append(combination.intro)
            user_combination_price.append(user_combination.price)
            user_combination_image.append(combination.image)
            user_combination_status_complete.append(user_combination.status)
            user_combination_status_comment.append(user_combination.status2)
            user_combination_ids.append(user_combination.id)
            user_combination_user_name.append(user_combination.name)


    return render_template("order_list.html",
                           user_name=user_name, ids=ids, start_time=start_time, number=number, tel=tel,
                           combination_name=combination_name, introduction=introduction, price=price, image=image,
                           status=status_complete, status_comment=status_comment,

                           target_user_name=target_user_name, target_ids=target_ids, target_name=target_name, target_start_time=target_start_time,
                           target_number=target_number, target_introduction=target_introduction, target_tel=target_tel,
                           target_image=target_image, target_price=target_price, target_status_complete=target_status_complete,
                           target_status_comment=target_status_comment,

                           user_combination_ids=user_combination_ids, user_combination_name=user_combination_name,
                           user_combination_start_time=user_combination_start_time, user_combination_number=user_combination_number,
                           user_combination_introduction=user_combination_introduction, user_combination_tel=user_combination_tel,
                           user_combination_image=user_combination_image, user_combination_price=user_combination_price,
                           user_combination_status_complete=user_combination_status_complete, user_combination_status_comment=user_combination_status_comment,
                           user_combination_user_name=user_combination_user_name)


@app.route('/transport_setID', methods=['GET', 'POST'])
def transport_setID():
    print("调用transport_setID函数了！")
    set_id = str(request.form.get('set_id'))
    print(set_id)
    session["set_id"] = set_id
    print("set id = ")
    print(set_id)
    return '0'


# @app.route('/staff/contents/store_plan_id', methods=['GET', 'POST'])
# def store_plan_id():
#     plan_id = request.args.get("plan_id")
#     session['plan_id'] = plan_id
#     return '0'


@app.route('/staff/contents/destinations/store_des_id', methods=['GET', 'POST'])
def delete_destination():
    des_id = request.args.get("id")
    session['des_id'] = des_id
    return '0'


@app.route('/staff/contents/destinations/store_attr_id', methods=['GET', 'POST'])
def delete_attraction():
    attr_id = request.args.get("id")
    session['attr_id'] = attr_id
    return '0'


@app.route('/staff/contents/destinations/store_acc_id', methods=['GET', 'POST'])
def delete_accommodation():
    acc_id = request.args.get("id")
    session['acc_id'] = acc_id
    return '0'


@app.route('/staff/contents/destinations/store_tra_id', methods=['GET', 'POST'])
def delete_traffic():
    tra_id = request.args.get("id")
    session['tra_id'] = tra_id
    return '0'


@app.route('/staff/pack_orders/store_order_id', methods=['GET', 'POST'])
def cancel_pack_orders():
    pack_order_id = request.args.get("id")
    session['pack_order_id'] = pack_order_id
    return '0'


@app.route('/staff/other_orders/store_order_id', methods=['GET', 'POST'])
def cancel_other_orders():
    other_order_id = request.args.get("id")
    session['other_order_id'] = other_order_id
    return '0'

# 查看order details
@app.route('/check_booking_details/<booking_id>', methods=['GET', 'POST'])
def check_booking_details(booking_id):
    booking = db.session.query(RecordC).filter(RecordC.id == booking_id).first()
    combination_id = booking.combination_id
    combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
    return render_template("orderDetail.html", booking=booking, combination=combination)

@app.route('/check_booking_target_details/<target_id>', methods=['GET', 'POST'])
def check_booking_target_details(target_id):
    target = db.session.query(Target).filter(Target.id == target_id).first()
    return render_template("orderDetail.html", target=target)

@app.route('/check_booking_combination_details/<combination_id>', methods=['GET', 'POST'])
def check_booking_combination_details(combination_id):
    booking = db.session.query(RecordP).filter(RecordP.id == combination_id).first()
    combination_id = booking.combination_id
    combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
    return render_template("orderDetail.html", booking=booking, combination=combination)


def translate(q):
    # 百度appid和密钥需要通过注册百度【翻译开放平台】账号后获得
    appid = '20230228001579285'  # 填写你的appid
    secretKey = 'i_i50GKeYlqZOVY7Q8HS'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'  # 原文语种
    toLang = 'en'  # 译文语种
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        # print('翻译：：')
        print(result)
        # print(type(result))
        re = result['trans_result'][0]['dst']
        print(re)

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


#跟我们联系! 邮箱自动回复
@app.route("/contact_email", methods=['GET', 'POST'])
def contact_email():
    # GET, POST
    name = request.form.get("name")
    message_content = request.form.get("message")
    email = request.form.get("email")
    print(message_content)

    if email:
        message = Message(
            subject="【Digital Beans】Feedback Received",
            recipients=[email],
            body=f"【Digital Beans】We have received your feedback, and we will contact you soon!\n\n" 
                 f" Note: this is an automatic reply!",
        )
        mail.send(message)
        # code:200 成功的正常的请求
        contact_message = ContactModel(email=email, name=name, message=message_content)
        db.session.add(contact_message)
        db.session.commit()
        flash("Send email successfully!")
        return redirect(url_for('contact_us'))
    else:
        # code: 40 客户端错误
        flash("Wrong in sending emails!")
        return redirect(url_for('contact_us'))

def changeBookingStatus():
    # 本身的combination
    bookings = db.session.query(RecordC).all()
    for book in bookings:
        book_id = book.id
        start_time = book.start_time
        current_time = datetime.now().strftime('%Y-%m-%d')

        combination_id = book.combination_id
        combination = db.session.query(Combination).filter_by(id=combination_id).first()
        length = combination.length

        start_datetime = datetime.strptime(start_time, '%Y-%m-%d')
        length_timedelta = timedelta(days=length)
        end_datetime = start_datetime + length_timedelta
        end_time = end_datetime.strftime('%Y-%m-%d')

        if end_time <= current_time:

            record = RecordC.query.filter_by(id=book_id).update({'status': 'Completed'})
            db.session.commit()

    # 客制化定制
    personal_bookings = db.session.query(RecordP).all()
    for book in personal_bookings:
        book_id = book.id
        start_time = book.start_time
        current_time = datetime.now().strftime('%Y-%m-%d')

        combination_id = book.combination_id
        combination = db.session.query(UserCombination).filter_by(id=combination_id).first()
        length = combination.length

        start_datetime = datetime.strptime(start_time, '%Y-%m-%d')
        length_timedelta = timedelta(days=length)
        end_datetime = start_datetime + length_timedelta
        end_time = end_datetime.strftime('%Y-%m-%d')

        if end_time <= current_time:
            record = RecordC.query.filter_by(id=book_id).update({'status': 'Completed'})
            db.session.commit()

    # target
    targets = db.session.query(Record).all()
    for book in targets:
        book_id = book.id
        start_time = book.start_time
        end_time = book.end_time
        current_time = datetime.now().strftime('%Y-%m-%d')

        target_id = book.target_id
        target = db.session.query(Target).filter_by(id=target_id).first()
        type = target.type
        if type == 1:
            # 住宿分天数
            if end_time <= current_time:
                record = Record.query.filter_by(id=book_id).update({'status': 'Completed'})
                db.session.commit()
        else:
            if start_time <= current_time:
                record = Record.query.filter_by(id=book_id).update({'status': 'Completed'})
                db.session.commit()




# 图片
@app.route("/improveImage", methods=['GET', 'POST'])
def improveImage():
    print("improveimage")
    APP_ID = '32717303'
    API_KEY = 'Tcbc4I8QOGersZaBYUjeMfM6'
    SECRET_KEY = 'I2QGn6cnrjuqtlSx08xRQfc00sGaWCXl'

    img = request.form.get("img_route")

    img_route = img[1:]
    print("img = ")
    print(img)

    # request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/dehaze"
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"
    # 二进制方式打开图片文件
    # f = open('./static/upload/2023042217125545.jpg', 'rb')
    f = open(img_route, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    # get token
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Tcbc4I8QOGersZaBYUjeMfM6&client_secret=I2QGn6cnrjuqtlSx08xRQfc00sGaWCXl&"
    response = requests.get(host)

    if response:
        j = response.json()
        access_token = j["access_token"]
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)

        if response:
            print(response.json())
            json = response.json()
            return json


def main():
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    changeBookingStatus()
    # app.run(debug=True, port=5000)
    set_logger(logger)
    socketio.run(app, allow_unsafe_werkzeug=True,debug=True, port=5001)
#<!--------------------chat------------------->


@app.route("/calendar", methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))
    user_id = current_user.id
    # 展示预定的combination
    days = db.session.query(RecordC).filter_by(user_id=user_id)
    dates = []
    destinations = []
    attractions = []
    accommodations = []
    traffics = []
    for day in days:
        start_time = day.start_time
        # start_t = datetime.strptime(start_time, '%Y-%m-%d')
        start_date = datetime.strptime(start_time, '%Y-%m-%d')
        dates.append(start_time)
        combination_id = day.combination_id
        combination = db.session.query(Combination).filter_by(id=combination_id).first()
        day_id = combination.day1
        day = db.session.query(Day).filter_by(id=day_id).first()

        # destinations
        destination_id = day.destination_id
        destination = db.session.query(Destination).filter_by(id=destination_id).first()
        destinations.append(destination.name)

        # attraction
        attraction_id = day.attraction_id
        attraction = db.session.query(Target).filter_by(id=attraction_id).first()
        # attractions.append(attraction)
        attraction_dict = {
            "name": attraction.name,
            "location": attraction.location,
            "image": attraction.image,
            "intro": attraction.intro,
            "price": attraction.price
        }
        attractions.append(attraction_dict)

        # accommodation
        accommodation_id = day.accommodation_id
        accommodation = db.session.query(Target).filter_by(id=accommodation_id).first()
        # accommodations.append(accommodation)
        accommodation_dict = {
            "name": accommodation.name,
            "location": accommodation.location,
            "image": accommodation.image,
            "intro": accommodation.intro,
            "price": accommodation.price
        }
        accommodations.append(accommodation_dict)

        # traffics
        traffic_id = day.traffic_id
        traffic = db.session.query(Target).filter_by(id=traffic_id).first()
        traffic_dict = {
            "name": traffic.name,
            "location": traffic.location,
            "image": traffic.image,
            "intro": traffic.intro,
            "price": traffic.price
        }
        traffics.append(traffic_dict)

        length = combination.length

        for i in range(0, length - 1):
            length_timedelta = timedelta(days=1)
            following_time = start_date + length_timedelta
            following_time_string = following_time.strftime('%Y-%m-%d')
            dates.append(following_time_string)
            start_date = following_time
            # time listtttttttt
            a = i + 1
            str_day = "day" + str(a)
            day_id = getattr(combination, str_day)
            day = db.session.query(Day).filter_by(id=day_id).first()

            # destinations
            destination_id = day.destination_id
            destination = db.session.query(Destination).filter_by(id=destination_id).first()
            destinations.append(destination.name)
            # attraction
            attraction_id = day.attraction_id
            attraction = db.session.query(Target).filter_by(id=attraction_id).first()
            # attractions.append(attraction)
            attraction_dict = {
                "name": attraction.name,
                "location": attraction.location,
                "image": attraction.image,
                "intro": attraction.intro,
                "price": attraction.price
            }
            attractions.append(attraction_dict)

            # accommodation
            accommodation_id = day.accommodation_id
            accommodation = db.session.query(Target).filter_by(id=accommodation_id).first()
            # accommodations.append(accommodation)
            accommodation_dict = {
                "name": accommodation.name,
                "location": accommodation.location,
                "image": accommodation.image,
                "intro": accommodation.intro,
                "price": accommodation.price
            }
            accommodations.append(accommodation_dict)

            # traffics
            traffic_id = day.traffic_id
            traffic = db.session.query(Target).filter_by(id=traffic_id).first()
            traffic_dict = {
                "name": traffic.name,
                "location": traffic.location,
                "image": traffic.image,
                "intro": traffic.intro,
                "price": traffic.price
            }
            traffics.append(traffic_dict)

    #展示客制化combination
    days = db.session.query(RecordP).filter_by(user_id=user_id)
    for day in days:
        start_time = day.start_time
        # start_t = datetime.strptime(start_time, '%Y-%m-%d')
        start_date = datetime.strptime(start_time, '%Y-%m-%d')
        dates.append(start_time)
        combination_id = day.combination_id
        combination = db.session.query(Combination).filter_by(id=combination_id).first()
        day_id = combination.day1
        day = db.session.query(Day).filter_by(id=day_id).first()

        # destinations
        destination_id = day.destination_id
        destination = db.session.query(Destination).filter_by(id=destination_id).first()
        destinations.append(destination.name)

        # attraction
        attraction_id = day.attraction_id
        attraction = db.session.query(Target).filter_by(id=attraction_id).first()
        # attractions.append(attraction)
        attraction_dict = {
            "name": attraction.name,
            "location": attraction.location,
            "image": attraction.image,
            "intro": attraction.intro,
            "price": attraction.price
        }
        attractions.append(attraction_dict)

        # accommodation
        accommodation_id = day.accommodation_id
        accommodation = db.session.query(Target).filter_by(id=accommodation_id).first()
        # accommodations.append(accommodation)
        accommodation_dict = {
            "name": accommodation.name,
            "location": accommodation.location,
            "image": accommodation.image,
            "intro": accommodation.intro,
            "price": accommodation.price
        }
        accommodations.append(accommodation_dict)

        # traffics
        traffic_id = day.traffic_id
        traffic = db.session.query(Target).filter_by(id=traffic_id).first()
        traffic_dict = {
            "name": traffic.name,
            "location": traffic.location,
            "image": traffic.image,
            "intro": traffic.intro,
            "price": traffic.price
        }
        traffics.append(traffic_dict)

        length = combination.length

        for i in range(0, length - 1):
            length_timedelta = timedelta(days=1)
            following_time = start_date + length_timedelta
            following_time_string = following_time.strftime('%Y-%m-%d')
            dates.append(following_time_string)
            start_date = following_time
            # time listtttttttt
            a = i + 1
            str_day = "day" + str(a)
            day_id = getattr(combination, str_day)
            day = db.session.query(Day).filter_by(id=day_id).first()

            # destinations
            destination_id = day.destination_id
            destination = db.session.query(Destination).filter_by(id=destination_id).first()
            destinations.append(destination.name)
            # attraction
            attraction_id = day.attraction_id
            attraction = db.session.query(Target).filter_by(id=attraction_id).first()
            # attractions.append(attraction)
            attraction_dict = {
                "name": attraction.name,
                "location": attraction.location,
                "image": attraction.image,
                "intro": attraction.intro,
                "price": attraction.price
            }
            attractions.append(attraction_dict)

            # accommodation
            accommodation_id = day.accommodation_id
            accommodation = db.session.query(Target).filter_by(id=accommodation_id).first()
            # accommodations.append(accommodation)
            accommodation_dict = {
                "name": accommodation.name,
                "location": accommodation.location,
                "image": accommodation.image,
                "intro": accommodation.intro,
                "price": accommodation.price
            }
            accommodations.append(accommodation_dict)

            # traffics
            traffic_id = day.traffic_id
            traffic = db.session.query(Target).filter_by(id=traffic_id).first()
            traffic_dict = {
                "name": traffic.name,
                "location": traffic.location,
                "image": traffic.image,
                "intro": traffic.intro,
                "price": traffic.price
            }
            traffics.append(traffic_dict)

    #展示单独预定target
    days = db.session.query(Record).filter_by(user_id=user_id)
    for day in days:
        start_time = day.start_time
        start_date = datetime.strptime(start_time, '%Y-%m-%d')
        day_id = day.target_id

        target = db.session.query(Target).filter_by(id=day_id).first()
        t = target.type
        print("target type")
        print(type(t))
        destinations.append("")
        # 预定的是住宿
        if t == 1:
            end_time = day.end_time
            end_date = datetime.strptime(end_time, '%Y-%m-%d')
            delta = end_date - start_date  # 计算日期差
            length = delta.days  # 获取日期差中的天数
            dates.append(start_time)

            for i in range(0, length - 1):
                length_timedelta = timedelta(days=1)
                following_time = start_date + length_timedelta
                following_time_string = following_time.strftime('%Y-%m-%d')
                dates.append(following_time_string)
                start_date = following_time

                accommodation_dict = {
                    "name": target.name,
                    "location": target.location,
                    "image": target.image,
                    "intro": target.intro,
                    "price": target.price
                }
                accommodations.append(accommodation_dict)

                attraction_dict = {
                    "name": "",
                    "location": "",
                    "image": "",
                    "intro": "",
                    "price": ""
                }
                attractions.append(attraction_dict)

                traffic_dict = {
                    "name": "",
                    "location":"",
                    "image": "",
                    "intro": "",
                    "price": ""
                }
                traffics.append(traffic_dict)

        #预定的是景点
        elif t == 0:
            print("单独预定景点")
            dates.append(start_time)

            attraction_dict = {
                "name": target.name,
                "location": target.location,
                "image": target.image,
                "intro": target.intro,
                "price": target.price
            }
            attractions.append(attraction_dict)
            accommodation_dict = {
                "name": "",
                "location": "",
                "image": "",
                "intro": "",
                "price": ""
            }
            accommodations.append(accommodation_dict)

            traffic_dict = {
                "name": "",
                "location": "",
                "image": "",
                "intro": "",
                "price": ""
            }
            traffics.append(traffic_dict)

    json_content = []
    d = {"date":dates}
    des = {"destination":destinations}
    at = {"attraction":attractions}
    ac = {"accommodation":accommodations}
    t = {"traffic":traffics}

    # 将其他字典添加到json_content列表中
    json_content.append(d)
    json_content.append(des)
    json_content.append(at)
    json_content.append(ac)
    json_content.append(t)

    return jsonify(json_content)

# testInfo = []
# @app.route("/data", methods=['GET', 'POST'])
# def data():
#     # testInfo['name'] = 'xiaoming'
#     # testInfo['age'] = '28'
#     # 使用datetime写2023年4月30日
#     date1 = datetime(2023, 5, 10, 0, 0, 0).strftime('%Y-%m-%d')
#     date2 = datetime(2023, 5, 11, 0, 0, 0).strftime('%Y-%m-%d')
#     date3 = datetime(2023, 5, 12, 0, 0, 0).strftime('%Y-%m-%d')
#     date4 = datetime(2023, 5, 13, 0, 0, 0).strftime('%Y-%m-%d')
#     date = [date1, date2, date3, date4]
#     return jsonify(date)

if __name__ == '__main__':
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    # openAI()
    app.run(debug=True, port=5000)

