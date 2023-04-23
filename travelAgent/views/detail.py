import requests
from flask import Blueprint

# from travelAgent.app import logger
from travelAgent.config import basedir

detail_blueprint = Blueprint(name="details", import_name=__name__)

import os
import this
import time
import base64

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
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, RecordC
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str

global set_id


# 图片
@detail_blueprint.route("/improveImage/<img>", methods=['GET', 'POST'])
def improveImage(img):
    print("improveimage")
    APP_ID = '32717303'
    API_KEY = 'Tcbc4I8QOGersZaBYUjeMfM6'
    SECRET_KEY = 'I2QGn6cnrjuqtlSx08xRQfc00sGaWCXl'

    # img = request.form.get("img_route")

    img_route = img[1:]
    print("img = ")
    print(img)

    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/dehaze"
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
            # img_r = json["image"]
            # route = "data:image/jpg;base64," + img_r
            return json

@detail_blueprint.route("/showSetDetails", methods=['GET', 'POST'])
def showSetDetails():
    print("调用showdetail函数了！")
    set_id = session.get("set_id")
    print(set_id)

    set = db.session.query(Combination).filter(Combination.id == set_id).first()
    ID = set_id
    length = set.length
    print(length)
    attractions=[]
    accomodations=[]
    traffic=[]

    comment_form = CommentForm(request.form)
    id = Random_str().create_uuid()


    if request.method == 'POST':

        print("ok2")
        print(comment_form.comment.data)

        if comment_form.validate_on_submit():

            # Images storage path
            file_dir = os.path.join(basedir, "static/upload/")
            # Getting the data transferred from the front end
            files = request.files.getlist('image')  # Gets the value of myfiles from ajax, of type list
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
            # check = db.session.query(CommentC).filter(CommentC.user_id == current_user.id, CommentC.combination_id == set_id).scalar()
            # check2 = db.session.query(CommentC).filter(CommentC.combination_id == set_id).scalar() is None
            print("77777788888")
            # print(check)
            check = True
            for comment in CommentC.query.filter(CommentC.combination_id == set_id, CommentC.user_id == current_user.id).all():
                if comment.content == comment_form.comment.data:
                    check = False
                    break
            if check:
                comment = CommentC(user_id=current_user.id, username=current_user.get_username(), combination_id=set_id,
                                   score=comment_form.score.data, content=comment_form.comment.data, image=path,
                                   time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                db.session.add(comment)

        if length == 1:
            day1_id = set.day1
            day1 = db.session.query(Day).filter(Day.id == day1_id).first()
            day1_att_id = day1.attraction_id
            day1_acc_id = day1.accommodation_id
            day1_tra_id = day1.traffic_id
            day1_attraction = db.session.query(Target).filter(Target.id == day1_att_id).first()
            day1_accommodation = db.session.query(Target).filter(Target.id == day1_acc_id).first()
            day1_traffic = db.session.query(Target).filter(Target.id == day1_tra_id).first()

            attractions.append(day1_attraction)

            accomodations.append(day1_accommodation)

            traffic.append(day1_traffic)

        elif length == 2:
            day1_id = set.day1
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

            attractions.append(day1_attraction)
            attractions.append(day2_attraction)

            accomodations.append(day1_accommodation)
            accomodations.append(day2_accommodation)

            traffic.append(day1_traffic)
            traffic.append(day2_traffic)

        elif length == 3:
            day1_id = set.day1
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

            attractions.append(day1_attraction)
            attractions.append(day2_attraction)
            attractions.append(day3_attraction)

            accomodations.append(day1_accommodation)
            accomodations.append(day2_accommodation)
            accomodations.append(day3_accommodation)

            traffic.append(day1_traffic)
            traffic.append(day2_traffic)
            traffic.append(day3_traffic)

        elif length == 4:
            day1_id = set.day1
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

            attractions.append(day1_attraction)
            attractions.append(day2_attraction)
            attractions.append(day3_attraction)
            attractions.append(day4_attraction)

            accomodations.append(day1_accommodation)
            accomodations.append(day2_accommodation)
            accomodations.append(day3_accommodation)
            accomodations.append(day4_accommodation)

            traffic.append(day1_traffic)
            traffic.append(day2_traffic)
            traffic.append(day3_traffic)
            traffic.append(day4_traffic)

        elif length == 5:

            day1_id = set.day1
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

            attractions.append(day1_attraction)
            attractions.append(day2_attraction)
            attractions.append(day3_attraction)
            attractions.append(day4_attraction)
            attractions.append(day5_attraction)

            accomodations.append(day1_accommodation)
            accomodations.append(day2_accommodation)
            accomodations.append(day3_accommodation)
            accomodations.append(day4_accommodation)
            accomodations.append(day5_accommodation)

            traffic.append(day1_traffic)
            traffic.append(day2_traffic)
            traffic.append(day3_traffic)
            traffic.append(day4_traffic)
            traffic.append(day5_traffic)

        elif length == 6:

            day1_id = set.day1
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

            attractions.append(day1_attraction)
            attractions.append(day2_attraction)
            attractions.append(day3_attraction)
            attractions.append(day4_attraction)
            attractions.append(day5_attraction)
            attractions.append(day6_attraction)

            accomodations.append(day1_accommodation)
            accomodations.append(day2_accommodation)
            accomodations.append(day3_accommodation)
            accomodations.append(day4_accommodation)
            accomodations.append(day5_accommodation)
            accomodations.append(day6_accommodation)

            traffic.append(day1_traffic)
            traffic.append(day2_traffic)
            traffic.append(day3_traffic)
            traffic.append(day4_traffic)
            traffic.append(day5_traffic)
            traffic.append(day6_traffic)

        else:

            print("else!!!")

            day1_id = set.day1
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

            attractions.append(day1_attraction)
            attractions.append(day2_attraction)
            attractions.append(day3_attraction)
            attractions.append(day4_attraction)
            attractions.append(day5_attraction)
            attractions.append(day6_attraction)
            attractions.append(day7_attraction)

            accomodations.append(day1_accommodation)
            accomodations.append(day2_accommodation)
            accomodations.append(day3_accommodation)
            accomodations.append(day4_accommodation)
            accomodations.append(day5_accommodation)
            accomodations.append(day6_accommodation)
            accomodations.append(day7_accommodation)

            traffic.append(day1_traffic)
            traffic.append(day2_traffic)
            traffic.append(day3_traffic)
            traffic.append(day4_traffic)
            traffic.append(day5_traffic)
            traffic.append(day6_traffic)
            traffic.append(day7_traffic)

        return render_template("travelRoutesDetail.html", current_user=current_user, comment_form=comment_form,
                               comments=db.session.query(CommentC).filter(CommentC.combination_id==set_id).all(), length=length, set=set, combination_id=set_id,
                               accomodations=accomodations, attractions=attractions, traffic=traffic)

    # if request.method == 'GET':

    comments = db.session.query(CommentC).filter(CommentC.combination_id==set_id).all()
    # comments = CommentC.query.filter.(CommentC.combination_id == set_id).all()
    # return render_template("travelRoutesDetail.html", comments=comments, comment_form=comment_form, length=length, set=set, combination_id=ID,
    #                        accomodations=accomodations, attractions=attractions, traffic=traffic)
    if length == 1:
        day1_id = set.day1
        day1 = db.session.query(Day).filter(Day.id == day1_id).first()
        day1_att_id = day1.attraction_id
        day1_acc_id = day1.accommodation_id
        day1_tra_id = day1.traffic_id
        day1_attraction = db.session.query(Target).filter(Target.id == day1_att_id).first()
        day1_accommodation = db.session.query(Target).filter(Target.id == day1_acc_id).first()
        day1_traffic = db.session.query(Target).filter(Target.id == day1_tra_id).first()

        attractions.append(day1_attraction)


        accomodations.append(day1_accommodation)


        traffic.append(day1_traffic)

    elif length == 2:
        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)


        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)


        traffic.append(day1_traffic)
        traffic.append(day2_traffic)

    elif length == 3:
        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)

        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)

    elif length == 4:
        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)


        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)


        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)

    elif length == 5:

        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)
        attractions.append(day5_attraction)


        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)
        accomodations.append(day5_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)
        traffic.append(day5_traffic)

    elif length == 6:

        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)
        attractions.append(day5_attraction)
        attractions.append(day6_attraction)

        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)
        accomodations.append(day5_accommodation)
        accomodations.append(day6_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)
        traffic.append(day5_traffic)
        traffic.append(day6_traffic)

    else:

        print("else!!!")

        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)
        attractions.append(day5_attraction)
        attractions.append(day6_attraction)
        attractions.append(day7_attraction)

        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)
        accomodations.append(day5_accommodation)
        accomodations.append(day6_accommodation)
        accomodations.append(day7_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)
        traffic.append(day5_traffic)
        traffic.append(day6_traffic)
        traffic.append(day7_traffic)

    return render_template("travelRoutesDetail.html", comments=comments, comment_form=comment_form, length=length,
                           set=set, combination_id=ID,
                           accomodations=accomodations, attractions=attractions, traffic=traffic)


# 展示booking细节的函数
@detail_blueprint.route("/showBookingDetail/<booking_id>")
def showBookingDetail(booking_id):
    booking = db.session.query(RecordC).filter(RecordC.id == booking_id).first()
    combination_id = booking.combination_id

    combination = db.session.query(Combination).filter(Combination.id == combination_id).first()
    length = combination.length

    attractions=[]
    accomodations=[]
    traffic=[]

    if length == 1:
        day1_id = set.day1
        day1 = db.session.query(Day).filter(Day.id == day1_id).first()
        day1_att_id = day1.attraction_id
        day1_acc_id = day1.accommodation_id
        day1_tra_id = day1.traffic_id
        day1_attraction = db.session.query(Target).filter(Target.id == day1_att_id).first()
        day1_accommodation = db.session.query(Target).filter(Target.id == day1_acc_id).first()
        day1_traffic = db.session.query(Target).filter(Target.id == day1_tra_id).first()

        attractions.append(day1_attraction)


        accomodations.append(day1_accommodation)


        traffic.append(day1_traffic)


    elif length == 2:
        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)


        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)


        traffic.append(day1_traffic)
        traffic.append(day2_traffic)


    elif length == 3:
        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)

        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)


    elif length == 4:
        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)


        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)


        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)

    elif length == 5:

        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)
        attractions.append(day5_attraction)


        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)
        accomodations.append(day5_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)
        traffic.append(day5_traffic)




    elif length == 6:

        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)
        attractions.append(day5_attraction)
        attractions.append(day6_attraction)

        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)
        accomodations.append(day5_accommodation)
        accomodations.append(day6_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)
        traffic.append(day5_traffic)
        traffic.append(day6_traffic)


    else:

        print("else!!!")

        day1_id = set.day1
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

        attractions.append(day1_attraction)
        attractions.append(day2_attraction)
        attractions.append(day3_attraction)
        attractions.append(day4_attraction)
        attractions.append(day5_attraction)
        attractions.append(day6_attraction)
        attractions.append(day7_attraction)

        accomodations.append(day1_accommodation)
        accomodations.append(day2_accommodation)
        accomodations.append(day3_accommodation)
        accomodations.append(day4_accommodation)
        accomodations.append(day5_accommodation)
        accomodations.append(day6_accommodation)
        accomodations.append(day7_accommodation)

        traffic.append(day1_traffic)
        traffic.append(day2_traffic)
        traffic.append(day3_traffic)
        traffic.append(day4_traffic)
        traffic.append(day5_traffic)
        traffic.append(day6_traffic)
        traffic.append(day7_traffic)


    return render_template("", length=length, combination=combination, booking=booking,
                               accomodations=accomodations, attractions=attractions, traffic=traffic)



