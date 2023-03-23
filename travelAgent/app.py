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
import datetime

import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str
from travelAgent.views.background import background_blueprint

# -------------------------------------register blueprints------------------------------------------
app.register_blueprint(login_blueprint)
app.register_blueprint(background_blueprint)

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
    Sets = Combination.query.all()
    return render_template("homepage.html", Sets=Sets)


@app.route('/homepage2', methods=['GET', 'POST'])
def homepage2():
    logger.info('Entered the HOME page')
    return render_template("homepage2.html")


@app.route('/admin')
def admin():
    return render_template("./background/dashboard.html")



@app.route('/travelRoutesDetail', methods=['GET', 'POST'])
def travel_routes_detail():
    # Create a unique id for the image
    id = Random_str().create_uuid()
    print(Comment.query.all())
    logger.info('Entered the TRAVEL ROUTE DETAIL page')
    comment_form = CommentForm(request.form)
    image_form = ImageForm(request.files)
    if comment_form.validate_on_submit() :

        # Images storage path
        file_dir = os.path.join(basedir, "static/upload/")
        # Getting the data transferred from the front end
        files = request.files.getlist('img')  # Gets the value of myfiles from ajax, of type list
        path = ""


        for img in files:
            # Extract the suffix of the uploaded image and
            # Name the image after the commodity id and store it in the specific path
            check = img.content_type
            # check if upload image
            if str(check) != 'application/octet-stream':
                fname = img.filename
                ext = fname.rsplit('.', 1)[1]
                new_filename = id + '.' + ext
                img.save(os.path.join(file_dir, new_filename))
                path = "../static/upload/" + new_filename

        # default: like=0 path=""
        comment = Comment(user_id=current_user.id, target_id=1,score = comment_form.score.data, content=comment_form.comment.data,image = path, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        db.session.add(comment)
        flash('已评论')
        return redirect(url_for('travel_routes_detail'))

    return render_template("travelRoutesDetail.html", current_user=current_user, comment_form=comment_form, comments=Comment.query.all())


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


def showSetDetails(ID):

    set = db.session.query(Combination).filter(Combination.id == ID).first()

    day1_id = set.day1
    print(day1_id)


    day1 = db.session.query(Day).filter(Day.id == day1_id).first()
    day1_att_id = day1.attraction_id
    day1_acc_id = day1.accommodation_id
    day1_tra_id = day1.traffic_id
    day1_attraction = db.session.query(Target).filter(Target.id == day1_att_id).first()
    day1_accommodation = db.session.query(Target).filter(Target.id == day1_acc_id).first()
    day1_traffic = db.session.query(Target).filter(Target.id == day1_tra_id).first()


    # day2的各种数据
    day2_id = set.day2
    day2 = db.session.query(Day).filter(Day.id == day2_id).first()
    day2_att_id = day2.attraction_id
    day2_acc_id = day2.accommodation_id
    day2_tra_id = day2.traffic_id
    day2_attraction = db.session.query(Target).filter(Target.id == day2_att_id).first()
    day2_accommodation = db.session.query(Target).filter(Target.id == day2_acc_id).first()
    day2_traffic = db.session.query(Target).filter(Target.id == day2_tra_id).first()


    # day3的各种数据
    day3_id = set.day3
    day3 = db.session.query(Day).filter(Day.id == day3_id).first()
    day3_att_id = day3.attraction_id
    day3_acc_id = day3.accommodation_id
    day3_tra_id = day3.traffic_id
    day3_attraction = db.session.query(Target).filter(Target.id == day3_att_id).first()
    day3_accommodation = db.session.query(Target).filter(Target.id == day3_acc_id).first()
    day3_traffic = db.session.query(Target).filter(Target.id == day3_tra_id).first()

    day4_id = set.day4
    day4 = db.session.query(Day).filter(Day.id == day4_id).first()
    day4_att_id = day4.attraction_id
    day4_acc_id = day4.accommodation_id
    day4_tra_id = day4.traffic_id
    day4_attraction = db.session.query(Target).filter(Target.id == day4_att_id).first()
    day4_accommodation = db.session.query(Target).filter(Target.id == day4_acc_id).first()
    day4_traffic = db.session.query(Target).filter(Target.id == day4_tra_id).first()

    day5_id = set.day5
    day5 = db.session.query(Day).filter(Day.id == day5_id).first()
    day5_att_id = day5.attraction_id
    day5_acc_id = day5.accommodation_id
    day5_tra_id = day5.traffic_id
    day5_attraction = db.session.query(Target).filter(Target.id == day5_att_id).first()
    day5_accommodation = db.session.query(Target).filter(Target.id == day5_acc_id).first()
    day5_traffic = db.session.query(Target).filter(Target.id == day5_tra_id).first()

    day6_id = set.day6
    day6 = db.session.query(Day).filter(Day.id == day6_id).first()
    day6_att_id = day6.attraction_id
    day6_acc_id = day6.accommodation_id
    day6_tra_id = day6.traffic_id
    day6_attraction = db.session.query(Target).filter(Target.id == day6_att_id).first()
    day6_accommodation = db.session.query(Target).filter(Target.id == day6_acc_id).first()
    day6_traffic = db.session.query(Target).filter(Target.id == day6_tra_id).first()

    day7_id = set.day7
    day7 = db.session.query(Day).filter(Day.id == day7_id).first()
    day7_att_id = day7.attraction_id
    day7_acc_id = day7.accommodation_id
    day7_tra_id = day7.traffic_id
    day7_attraction = db.session.query(Target).filter(Target.id == day7_att_id).first()
    day7_accommodation = db.session.query(Target).filter(Target.id == day7_acc_id).first()
    day7_traffic = db.session.query(Target).filter(Target.id == day7_tra_id).first()

    # 细节界面
    return render_template("test.html", day1_attraction=day1_attraction, day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                           day2_attraction=day2_attraction, day2_accommodation=day2_accommodation, day2_traffic=day2_traffic,
                           day3_attraction=day3_attraction, day3_accommodation=day3_accommodation, day3_traffic=day3_traffic,
                           day4_attraction=day4_attraction, day4_accommodation=day4_accommodation, day4_traffic=day4_traffic,
                           day5_attraction=day5_attraction, day5_accommodation=day5_accommodation, day5_traffic=day5_traffic,
                           day6_attraction=day6_attraction, day6_accommodation=day6_accommodation, day6_traffic=day6_traffic,
                           day7_attraction=day7_attraction, day7_accommodation=day7_accommodation, day7_traffic=day7_traffic)



if __name__ == '__main__':
    # showSetDetails(1)
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)

