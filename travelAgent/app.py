import os
import this
import time

from flask import Flask, render_template, request, flash, redirect, url_for, session
import logging
import http.client
import hashlib
import urllib
import random
import json
import datetime

import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, User, RecordC

from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str
from travelAgent.views.staff_site import staff_blueprint
from travelAgent.views.detail import detail_blueprint, showSetDetails
from travelAgent.views.search import search_blueprint
from travelAgent.views.favorite import favorite_blueprint
from travelAgent.views.booking import booking_blueprint


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
    if current_user.is_authenticated:
        return render_template("index.html", current_user=current_user)
    return render_template("index.html", current_user=None, username=None)


@app.route('/about')
def about():
    logger.info('Entered the ABOUT page')
    return render_template("about.html")


@app.route('/contactUs')
def contact_us():
    logger.info('Entered the CONTACT page')
    return render_template("contact.html")


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    logger.info('Entered the HOME page')
    Sets = Combination.query.all()
    print("homepage2")
    return render_template("homepage2.html", Sets=Sets)


# @app.route('/homepage2', methods=['GET', 'POST'])
# def homepage2():
#     logger.info('Entered the HOME page')
#     Sets = Combination.query.all()
#     print("homepage2")
#     return render_template("homepage2.html", Sets=Sets)

@app.route('/book', methods=['GET', 'POST'])
def book():
    logger.info('Entered the BOOK page')
    return render_template("book.html")


@app.route('/profile')
def profile():

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

        name = []
        introduction = []
        price = []
        image = []

    for book in bookings:
        combination_id = book.combination_id
        print(combination_id)
        combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
        name.append(combination.name)
        introduction.append(combination.intro)
        price.append(combination.price)
        image.append(combination.image)

    return render_template("profile.html", user=user, book=book, bookings=bookings,
                           name=name, introduction=introduction, price=price, image=image)


@app.route('/favourites')
def favourites():
    logger.info('Entered the FAVOURITES page')
    return render_template('favourites.html')


@app.route('/order_list')
def order_list():
    logger.info('Entered the order_list page')
    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))
    else:
        customer_id = current_user.id
        # 传递user的个人信息
        user = db.session.query(User).filter(User.id == customer_id).first()
        # 传输个人的booking记录
        # book = db.session.query(RecordC).filter(RecordC.user_id == customer_id).first()
        bookings = db.session.query(RecordC).filter(RecordC.user_id == customer_id).all()
        # combination中的信息

        name = []
        introduction = []
        price = []
        image = []

    for book in bookings:
        combination_id = book.combination_id
        print(combination_id)
        combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
        name.append(combination.name)
        introduction.append(combination.intro)
        price.append(combination.price)
        image.append(combination.image)

    return render_template("order_list.html", bookings=bookings,
                           name=name, introduction=introduction, price=price, image=image)


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
    print(plan_id)
    return '0'


# @app.route('/staff')
# def staff():
#     return render_template("./staff_site/base.html")
#
#
# @app.route('/staff1')
# def staff1():
#     return render_template("./staff_site/pages/index/index.html")
#
#
# @app.route('/staff2')
# def staff2():
#     print("sdfasdf")
#     return render_template("./staff_site/pages/ui-features/buttons.html")


# @app.route('/travelRoutesDetail', methods=['GET', 'POST'])
# def travel_routes_detail():
#     # Create a unique id for the image
#     id = Random_str().create_uuid()
#     # print(CommentC.query.all())
#     logger.info('Entered the TRAVEL ROUTE DETAIL page')
#     comment_form = CommentForm(request.form)
#     image_form = ImageForm(request.files)
#     if request.method == 'POST':
#         if comment_form.validate_on_submit():
#
#             # Images storage path
#             file_dir = os.path.join(basedir, "static/upload/")
#             # Getting the data transferred from the front end
#             files = request.files.getlist('img')  # Gets the value of myfiles from ajax, of type list
#             path = ""
#
#             for img in files:
#                 # Extract the suffix of the uploaded image and
#                 # Name the image after the commodity id and store it in the specific path
#                 check = img.content_type
#                 # check if upload image
#                 if str(check) != 'application/octet-stream':
#                     fname = img.filename
#                     ext = fname.rsplit('.', 1)[1]
#                     new_filename = id + '.' + ext
#                     img.save(os.path.join(file_dir, new_filename))
#                     path = "../static/upload/" + new_filename
#
#             # default: like=0 path=""
#             comment = CommentC(user_id=current_user.id, username=current_user.get_username(), combination_id=1,score=comment_form.score.data, content=comment_form.comment.data,image = path, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#             db.session.add(comment)
#             flash('已评论')
#             return redirect(url_for('travel_routes_detail'))
#
#         return render_template("travelRoutesDetail.html", current_user=current_user, comment_form=comment_form, comments=CommentC.query.all())
#     if request.method == 'GET':
#         comments = CommentC.query.all()
#         return render_template("travelRoutesDetail.html", comments=comments, comment_form=comment_form)


# 翻译功能 (auto - 英)
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



#<!--------------------chat------------------->
def main():
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    # app.run(debug=True, port=5000)
    set_logger(logger)
    socketio.run(app, allow_unsafe_werkzeug=True,debug=True, port=5001)
#<!--------------------chat------------------->


if __name__ == '__main__':
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)
