from flask import Blueprint

detail_blueprint = Blueprint(name="travel_route_detail", import_name=__name__)

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


@detail_blueprint.route("/showSetDetail/<set_id>")
def showSetDetails(set_id):
    print("调用showdetail函数了！")

    set = db.session.query(Combination).filter(Combination.id == set_id).first()

    length = set.length
    print(length)

    if length == 1:
        day1_id = set.day1
        day1 = db.session.query(Day).filter(Day.id == day1_id).first()
        day1_att_id = day1.attraction_id
        day1_acc_id = day1.accommodation_id
        day1_tra_id = day1.traffic_id
        day1_attraction = db.session.query(Target).filter(Target.id == day1_att_id).first()
        day1_accommodation = db.session.query(Target).filter(Target.id == day1_acc_id).first()
        day1_traffic = db.session.query(Target).filter(Target.id == day1_tra_id).first()
        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction,
                               day1_accommodation=day1_accommodation, day1_traffic=day1_traffic)
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

        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction,
                               day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                               day2_attraction=day2_attraction, day2_accommodation=day2_accommodation,
                               day2_traffic=day2_traffic)

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

        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction,
                               day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                               day2_attraction=day2_attraction, day2_accommodation=day2_accommodation,
                               day2_traffic=day2_traffic,
                               day3_attraction=day3_attraction, day3_accommodation=day3_accommodation,
                               day3_traffic=day3_traffic)

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

        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction,
                               day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                               day2_attraction=day2_attraction, day2_accommodation=day2_accommodation,
                               day2_traffic=day2_traffic,
                               day3_attraction=day3_attraction, day3_accommodation=day3_accommodation,
                               day3_traffic=day3_traffic,
                               day4_attraction=day4_attraction, day4_accommodation=day4_accommodation,
                               day4_traffic=day4_traffic)

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

        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction,
                               day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                               day2_attraction=day2_attraction, day2_accommodation=day2_accommodation,
                               day2_traffic=day2_traffic,
                               day3_attraction=day3_attraction, day3_accommodation=day3_accommodation,
                               day3_traffic=day3_traffic,
                               day4_attraction=day4_attraction, day4_accommodation=day4_accommodation,
                               day4_traffic=day4_traffic,
                               day5_attraction=day5_attraction, day5_accommodation=day5_accommodation,
                               day5_traffic=day5_traffic)



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

        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction,
                               day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                               day2_attraction=day2_attraction, day2_accommodation=day2_accommodation,
                               day2_traffic=day2_traffic,
                               day3_attraction=day3_attraction, day3_accommodation=day3_accommodation,
                               day3_traffic=day3_traffic,
                               day4_attraction=day4_attraction, day4_accommodation=day4_accommodation,
                               day4_traffic=day4_traffic,
                               day5_attraction=day5_attraction, day5_accommodation=day5_accommodation,
                               day5_traffic=day5_traffic,
                               day6_attraction=day6_attraction, day6_accommodation=day6_accommodation,
                               day6_traffic=day6_traffic)

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

        print(day7_traffic.intro)

        # 细节界面
        return render_template("travelRoutesDetail.html", day1_attraction=day1_attraction, day1_accommodation=day1_accommodation, day1_traffic=day1_traffic,
                               day2_attraction=day2_attraction, day2_accommodation=day2_accommodation, day2_traffic=day2_traffic,
                               day3_attraction=day3_attraction, day3_accommodation=day3_accommodation, day3_traffic=day3_traffic,
                               day4_attraction=day4_attraction, day4_accommodation=day4_accommodation, day4_traffic=day4_traffic,
                               day5_attraction=day5_attraction, day5_accommodation=day5_accommodation, day5_traffic=day5_traffic,
                               day6_attraction=day6_attraction, day6_accommodation=day6_accommodation, day6_traffic=day6_traffic,
                               day7_attraction=day7_attraction, day7_accommodation=day7_accommodation, day7_traffic=day7_traffic)