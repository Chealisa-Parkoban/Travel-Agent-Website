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
import numpy as np
import cv2

from datetime import datetime, timedelta
from aip import AipImageProcess

import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, User, RecordC, ContactModel
from flask_mail import Message

from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str
from travelAgent.views.staff_site import staff_blueprint
from travelAgent.views.detail import detail_blueprint, showSetDetails
from travelAgent.views.search import search_blueprint
from travelAgent.views.favorite import favorite_blueprint
from travelAgent.views.booking import booking_blueprint
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


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    logger.info('Entered the HOME page')
    changeBookingStatus()
    Sets = Combination.query.all()
    attractions = Target.query.filter(Target.type == '0').all()
    attractions = attractions[::-1]
    hotels = Target.query.filter(Target.type == '1').all()
    print("homepage2")
    return render_template("homepage2.html", Sets=Sets, attractions=attractions, hotels=hotels)


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

    print(user_name)

    return render_template("order_list.html", bookings=bookings, user_name=user_name, start_time=start_time, number=number, tel=tel,
                           combination_name=combination_name, introduction=introduction, price=price, image=image, status=status_complete, status_comment=status_comment)


@app.route('/transport_setID', methods=['GET', 'POST'])
def transport_setID():
    print("调用transport_setID函数了！")
    set_id = str(request.form.get('set_id'))
    print(set_id)
    session["set_id"] = set_id
    print("set id = ")
    print(set_id)
    return '0'


@app.route('/staff/contents/store_plan_id', methods=['GET', 'POST'])
def store_plan_id():
    plan_id = request.args.get("plan_id")
    session['plan_id'] = plan_id
    return '0'


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
    bookings = db.session.query(RecordC).all()
    for book in bookings:
        book_id = book.id
        start_time = book.start_time
        current_time = datetime.now().strftime('%Y-%m-%d')

        combination_id = book.combination_id
        combination = db.session.query(Combination).filter_by(id=combination_id).first()
        length = combination.length

        start_datetime = datetime.strptime(start_time, '%Y-%m-%d')
        # delta = datetime.timedelta(days=length)
        length_timedelta = timedelta(days=length)
        end_datetime = start_datetime + length_timedelta
        end_time = end_datetime.strftime('%Y-%m-%d')

        print("end_time: ")
        print(end_time)

        if end_time <= current_time:
            print("if 时间")
            record = RecordC.query.filter_by(id=book_id).update({'status': 'Completed'})
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


def openAI():
    # Apply the API key
    openai.api_key = "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"

    # Define the text prompt
    prompt = "how are u"

    # Generate completions using the API
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the message from the API response
    message = completions.choices[0].text
    print(message)
    return message




def main():
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    changeBookingStatus()
    # app.run(debug=True, port=5000)
    set_logger(logger)
    socketio.run(app, allow_unsafe_werkzeug=True,debug=True, port=5001)
#<!--------------------chat------------------->



# trytrytry
# class OpenAI_Request(object):
# #
#     def __init__(self,key,model_name,request_address):
#         super().__init__()
#         self.headers = {"Authorization":f"Bearer {key}","Content-Type": "application/json"}
#         self.model__name = model_name
#         self.request_address = request_address
#
#     def post_request(self,message):
#
#         data = {
#             "model": self.model__name,
#             "messages":  message
#         }
#         data = json.dumps(data)
#
#         response = requests.post(self.request_address, headers=self.headers, data=data)
#
#         return response
#
#
# if __name__ == '__main__':
#     keys = "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"
#     model_name = "gpt-3.5-turbo"
#     request_address = "https://api.openai.com/v1/chat/completions"
#     requestor = OpenAI_Request(keys,model_name,request_address)
#
#     while 1:
#         input_s = input('user input: ')
#         res = requestor.post_request(input_s)
#
#         response = res.json()['choices'][0]['message']['content']
#
#         if  response:
#             requestor.context_handler.append_cur_to_context(response,tag=1)
#
#         print(f"chatGPT: {response}")



if __name__ == '__main__':
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    # openAI()
    app.run(debug=True, port=5000)

