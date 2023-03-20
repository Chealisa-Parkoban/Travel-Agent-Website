import os
import this
import time

from flask import Flask, render_template, request, flash, redirect, url_for
import logging
import http.client
import hashlib
import urllib
import random
import json

import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm
from travelAgent.models import CommentC, SimpleComment, Combination , Day, Target , Destination
from travelAgent.views.login_handler import login_blueprint, current_user

# -------------------------------------register blueprints------------------------------------------
app.register_blueprint(login_blueprint)

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
    return render_template("homepage.html")


@app.route('/travelRoutesDetail', methods=['GET', 'POST'])
def travel_routes_detail():
    print(SimpleComment.query.all())
    logger.info('Entered the TRAVEL ROUTE DETAIL page')
    comment_form = CommentForm(request.form)
    if comment_form.validate_on_submit():
        comment = SimpleComment(username=current_user.username, content=comment_form.comment.data, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        db.session.add(comment)
        flash('已评论')
        return redirect(url_for('travel_routes_detail'))
    return render_template("travelRoutesDetail.html", current_user=current_user, comment_form=comment_form, comments=SimpleComment.query.all())


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



def showAllSets():
    jList = []
    # Extracting data from the database that is needed to display products
    sets = db.session.query(Combination.id, Combination.day1, Combination.day2, Combination.day3,
                                 Combination.day4,Combination.day5,Combination.day6,Combination.day7).all()
    # Processing of each message
    for piece in sets:
        # destination名字
        des = db.session.query(Destination).filter(Destination.id == piece[0]).first()
        destination = des.name

        # day1 的各种数据
        day1 = db.session.query(Day).filter(Day.id == piece[1]).first()
        day1_att_id = day1.attraction_id
        day1_acc_id = day1.accommodation_id
        day1_tra_id = day1.traffic_id
        day1_att = db.session.query(Target).filter(Target.id == day1_att_id ).first()
        day1_acc = db.session.query(Target).filter(Target.id == day1_acc_id).first()
        day1_tra = db.session.query(Target).filter(Target.id == day1_tra_id).first()
        day1_accommodation = day1_acc.name
        day1_attraction = day1_att.name
        day1_traffic = day1_tra.name
        day1_accommodation_intro = day1_acc.intro
        day1_attraction_intro = day1_att.intro
        day1_traffic_intro = day1_tra.intro
        day1_accommodation_image = day1_acc.image
        day1_attraction_intro = day1_att.image
        day1_traffic_intro = day1_tra.image
        day1_accommodation_price = day1_acc.price
        day1_attraction_price = day1_att.price
        day1_traffic_price = day1_tra.price

        # day2的各种数据
        day2 = db.session.query(Day).filter(Day.id == piece[2]).first()
        day2_att_id = day2.attraction_id
        day2_acc_id = day2.accommodation_id
        day2_tra_id = day2.traffic_id
        day2_att = db.session.query(Target).filter(Target.id == day2_att_id).first()
        day2_acc = db.session.query(Target).filter(Target.id == day2_acc_id).first()
        day2_tra = db.session.query(Target).filter(Target.id == day2_tra_id).first()
        day2_accommodation = day2_acc.name
        day2_attraction = day2_att.name
        day2_traffic = day2_tra.name
        day2_accommodation_intro = day2_acc.intro
        day2_attraction_intro = day2_att.intro
        day2_traffic_intro = day2_tra.intro
        day2_accommodation_image = day2_acc.image
        day2_attraction_intro = day2_att.image
        day2_traffic_intro = day2_tra.image
        day2_accommodation_price = day2_acc.price
        day2_attraction_price = day2_att.price
        day2_traffic_price = day2_tra.price

        # day3的各种数据
        day3 = db.session.query(Day).filter(Day.id == piece[3]).first()
        day3_att_id = day3.attraction_id
        day3_acc_id = day3.accommodation_id
        day3_tra_id = day3.traffic_id
        day3_att = db.session.query(Target).filter(Target.id == day3_att_id).first()
        day3_acc = db.session.query(Target).filter(Target.id == day3_acc_id).first()
        day3_tra = db.session.query(Target).filter(Target.id == day3_tra_id).first()
        day3_accommodation = day3_acc.name
        day3_attraction = day3_att.name
        day3_traffic = day3_tra.name
        day3_accommodation_intro = day3_acc.intro
        day3_attraction_intro = day3_att.intro
        day3_traffic_intro = day3_tra.intro
        day3_accommodation_image = day3_acc.image
        day3_attraction_intro = day3_att.image
        day3_traffic_intro = day3_tra.image
        day3_accommodation_price = day3_acc.price
        day3_attraction_price = day3_att.price
        day3_traffic_price = day3_tra.price

        day4 = db.session.query(Day).filter(Day.id == piece[4]).first()
        day4_att_id = day4.attraction_id
        day4_acc_id = day4.accommodation_id
        day4_tra_id = day4.traffic_id
        day4_att = db.session.query(Target).filter(Target.id == day4_att_id).first()
        day4_acc = db.session.query(Target).filter(Target.id == day4_acc_id).first()
        day4_tra = db.session.query(Target).filter(Target.id == day4_tra_id).first()
        day4_accommodation = day4_acc.name
        day4_attraction = day4_att.name
        day4_traffic = day4_tra.name
        day4_accommodation_intro = day4_acc.intro
        day4_attraction_intro = day4_att.intro
        day4_traffic_intro = day4_tra.intro
        day4_accommodation_image = day4_acc.image
        day4_attraction_intro = day4_att.image
        day4_traffic_intro = day4_tra.image
        day4_accommodation_price = day4_acc.price
        day4_attraction_price = day4_att.price
        day4_traffic_price = day4_tra.price

        day5 = db.session.query(Day).filter(Day.id == piece[5]).first()
        day5_att_id = day5.attraction_id
        day5_acc_id = day5.accommodation_id
        day5_tra_id = day5.traffic_id
        day5_att = db.session.query(Target).filter(Target.id == day5_att_id).first()
        day5_acc = db.session.query(Target).filter(Target.id == day5_acc_id).first()
        day5_tra = db.session.query(Target).filter(Target.id == day5_tra_id).first()
        day5_accommodation = day5_acc.name
        day5_attraction = day5_att.name
        day5_traffic = day5_tra.name
        day5_accommodation_intro = day5_acc.intro
        day5_attraction_intro = day5_att.intro
        day5_traffic_intro = day5_tra.intro
        day5_accommodation_image = day5_acc.image
        day5_attraction_intro = day5_att.image
        day5_traffic_intro = day5_tra.image
        day5_accommodation_price = day5_acc.price
        day5_attraction_price = day5_att.price
        day5_traffic_price = day5_tra.price

        day6 = db.session.query(Day).filter(Day.id == piece[6]).first()
        day6_att_id = day6.attraction_id
        day6_acc_id = day6.accommodation_id
        day6_tra_id = day6.traffic_id
        day6_att = db.session.query(Target).filter(Target.id == day6_att_id).first()
        day6_acc = db.session.query(Target).filter(Target.id == day6_acc_id).first()
        day6_tra = db.session.query(Target).filter(Target.id == day6_tra_id).first()
        day6_accommodation = day6_acc.name
        day6_attraction = day6_att.name
        day6_traffic = day6_tra.name
        day6_accommodation_intro = day6_acc.intro
        day6_attraction_intro = day6_att.intro
        day6_traffic_intro = day6_tra.intro
        day6_accommodation_image = day6_acc.image
        day6_attraction_intro = day6_att.image
        day6_traffic_intro = day6_tra.image
        day6_accommodation_price = day6_acc.price
        day6_attraction_price = day6_att.price
        day6_traffic_price = day6_tra.price

        day7 = db.session.query(Day).filter(Day.id == piece[7]).first()
        day7_att_id = day7.attraction_id
        day7_acc_id = day7.accommodation_id
        day7_tra_id = day7.traffic_id
        day7_att = db.session.query(Target).filter(Target.id == day7_att_id).first()
        day7_acc = db.session.query(Target).filter(Target.id == day7_acc_id).first()
        day7_tra = db.session.query(Target).filter(Target.id == day7_tra_id).first()
        day7_accommodation = day7_acc.name
        day7_attraction = day7_att.name
        day7_traffic = day7_tra.name
        day7_accommodation_intro = day7_acc.intro
        day7_attraction_intro = day7_att.intro
        day7_traffic_intro = day7_tra.intro
        day7_accommodation_image = day7_acc.image
        day7_attraction_intro = day7_att.image
        day7_traffic_intro = day7_tra.image
        day7_accommodation_price = day7_acc.price
        day7_attraction_price = day7_att.price
        day7_traffic_price = day7_tra.price

        # Processing data in dictionary form
        data = {}
        data["destination"] = destination
        data["day1_acc"] = day1_accommodation
        data["day1_att"] = day1_attraction
        data["day1_tra"] = day1_traffic
        data["day2_acc"] = day2_accommodation
        data["day2_att"] = day2_attraction
        data["day2_tra"] = day2_traffic
        data["day3_acc"] = day3_accommodation
        data["day3_att"] = day3_attraction
        data["day3_tra"] = day3_traffic
        data["day4_acc"] = day4_accommodation
        data["day4_att"] = day4_attraction
        data["day4_tra"] = day4_traffic
        data["day5_acc"] = day5_accommodation
        data["day5_att"] = day5_attraction
        data["day5_tra"] = day5_traffic
        data["day6_acc"] = day6_accommodation
        data["day6_att"] = day6_attraction
        data["day6_tra"] = day6_traffic
        data["day7_acc"] = day7_accommodation
        data["day7_att"] = day7_attraction
        data["day7_tra"] = day7_traffic

        # Dictionary to json
        # data2 is a piece of data in database in json
        data2 = json.dumps(data)
        jList.append(data2)

    # list to json
    str_json = json.dumps(jList, ensure_ascii=False, indent=2)

    return str_json


if __name__ == '__main__':

    # q = "how are you"
    # result = translate(q)  # 百度翻译
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)

