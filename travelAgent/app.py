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
from travelAgent.models import CommentC, Comment
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str

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
    # Create a unique id for the commodity
    id = Random_str().create_uuid()
    print(Comment.query.all())
    logger.info('Entered the TRAVEL ROUTE DETAIL page')
    comment_form = CommentForm(request.form)
    image_form = ImageForm(request.files)
    # logger.info('777777777777777')
    # logger.info(image_form.img.data.filename)

    # logger.info(request.files.getlist('img'))
    if comment_form.validate_on_submit() :
        logger.info('777777777777777')
        logger.info(basedir)

        # Images storage path
        file_dir = os.path.join(basedir, "static/upload/")
        logger.info('888888888')
        logger.info(file_dir)
        # Getting the data transferred from the front end
        files = request.files.getlist('img')  # Gets the value of myfiles from ajax, of type list
        path = ""

        for img in files:
            # Extract the suffix of the uploaded image and
            # Name the image after the commodity id and store it in the specific path
            fname = img.filename
            logger.info('9999999999999999')
            logger.info(fname)
            ext = fname.rsplit('.', 1)[1]
            new_filename = id + '.' + ext
            img.save(os.path.join(file_dir, new_filename))
            path = "../static/upload/" + new_filename
        comment = Comment(user_id=current_user.id, target_id=1,score = comment_form.score.data, content=comment_form.comment.data,image = path, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # comment = SimpleComment(username=current_user.username, content=comment_form.comment.data, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
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


if __name__ == '__main__':

    # q = "how are you"
    # result = translate(q)  # 百度翻译
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)

