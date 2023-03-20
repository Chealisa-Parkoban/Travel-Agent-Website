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
        day1_accommodation = day1.acc.name
        day1_attraction = day1.att.name
        day1_travel = day1.tra.name

        # day2的各种数据
        day2 = db.session.query(Day).filter(Day.id == piece[2]).first()
        day2_att_id = day2.attraction_id
        day2_acc_id = day2.accommodation_id
        day2_tra_id = day2.traffic_id
        day2_att = db.session.query(Target).filter(Target.id == day2_att_id).first()
        day2_acc = db.session.query(Target).filter(Target.id == day2_acc_id).first()
        day2_tra = db.session.query(Target).filter(Target.id == day2_tra_id).first()
        day2_accommodation = day2.acc.name
        day2_attraction = day2.att.name
        day2_travel = day2.tra.name

        # day3的各种数据
        day3 = db.session.query(Day).filter(Day.id == piece[3]).first()
        day3_att_id = day3.attraction_id
        day3_acc_id = day3.accommodation_id
        day3_tra_id = day3.traffic_id
        day3_att = db.session.query(Target).filter(Target.id == day3_att_id).first()
        day3_acc = db.session.query(Target).filter(Target.id == day3_acc_id).first()
        day3_tra = db.session.query(Target).filter(Target.id == day3_tra_id).first()
        day3_accommodation = day3.acc.name
        day3_attraction = day3.att.name
        day3_travel = day3.tra.name

        day4 = db.session.query(Day).filter(Day.id == piece[4]).first()
        day4_att_id = day4.attraction_id
        day4_acc_id = day4.accommodation_id
        day4_tra_id = day4.traffic_id
        day4_att = db.session.query(Target).filter(Target.id == day4_att_id).first()
        day4_acc = db.session.query(Target).filter(Target.id == day4_acc_id).first()
        day4_tra = db.session.query(Target).filter(Target.id == day4_tra_id).first()
        day4_accommodation = day4.acc.name
        day4_attraction = day4.att.name
        day4_travel = day4.tra.name

        day5 = db.session.query(Day).filter(Day.id == piece[5]).first()
        day5_att_id = day5.attraction_id
        day5_acc_id = day5.accommodation_id
        day5_tra_id = day5.traffic_id
        day5_att = db.session.query(Target).filter(Target.id == day5_att_id).first()
        day5_acc = db.session.query(Target).filter(Target.id == day5_acc_id).first()
        day5_tra = db.session.query(Target).filter(Target.id == day5_tra_id).first()
        day5_accommodation = day5.acc.name
        day5_attraction = day5.att.name
        day5_travel = day5.tra.name

        day6 = db.session.query(Day).filter(Day.id == piece[6]).first()
        day6_att_id = day6.attraction_id
        day6_acc_id = day6.accommodation_id
        day6_tra_id = day6.traffic_id
        day6_att = db.session.query(Target).filter(Target.id == day6_att_id).first()
        day6_acc = db.session.query(Target).filter(Target.id == day6_acc_id).first()
        day6_tra = db.session.query(Target).filter(Target.id == day6_tra_id).first()
        day6_accommodation = day6.acc.name
        day6_attraction = day6.att.name
        day6_travel = day6.tra.name

        day7 = db.session.query(Day).filter(Day.id == piece[7]).first()
        day7_att_id = day7.attraction_id
        day7_acc_id = day7.accommodation_id
        day7_tra_id = day7.traffic_id
        day7_att = db.session.query(Target).filter(Target.id == day7_att_id).first()
        day7_acc = db.session.query(Target).filter(Target.id == day7_acc_id).first()
        day7_tra = db.session.query(Target).filter(Target.id == day7_tra_id).first()
        day7_accommodation = day7.acc.name
        day7_attraction = day7.att.name
        day7_travel = day7.tra.name

        # Processing data in dictionary form
        data = {}
        data["destination"] = destination
        data["day1_acc"] = day1_accommodation
        data["day1_att"] = day1_attraction
        data["day1_tra"] = day1_travel
        data["day2_acc"] = day2_accommodation
        data["day2_att"] = day2_attraction
        data["day2_tra"] = day2_travel
        data["day3_acc"] = day3_accommodation
        data["day3_att"] = day3_attraction
        data["day3_tra"] = day3_travel
        data["day4_acc"] = day4_accommodation
        data["day4_att"] = day4_attraction
        data["day4_tra"] = day4_travel
        data["day5_acc"] = day5_accommodation
        data["day5_att"] = day5_attraction
        data["day5_tra"] = day5_travel
        data["day6_acc"] = day6_accommodation
        data["day6_att"] = day6_attraction
        data["day6_tra"] = day6_travel
        data["day7_acc"] = day7_accommodation
        data["day7_att"] = day7_attraction
        data["day7_tra"] = day7_travel

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

