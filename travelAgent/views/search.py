from flask import Blueprint
from flask import session
from sqlalchemy import text

search_blueprint = Blueprint(name="search", import_name=__name__)

import os
import this
import time

from flask import Flask, render_template, request, flash, redirect, url_for, sessions
import logging
import http.client
import hashlib
import urllib
import random
import json
import datetime
from sqlalchemy import or_, and_

import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, RecordC
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str

# test

@search_blueprint.route("/search_for_route", methods=['GET', 'POST'])
def search():
    destination = request.form.get('Destination')
    attraction = request.form.get('Attraction')
    price_up = request.form.get('Highest')
    price_low = request.form.get('Lowest')

    combination = []

    # 条件判断
    if (price_low > price_up) or (price_low < 0 ) or ( price_up < 0):
        flash('Wrong input! Please enter again')
        # redirect to the login page, for user to login
        return redirect(url_for("app.homepage"))

    else:

        # 只搜索combination
        if (destination is not None) and (attraction == "") and (price_up == "") and (price_low == ""):

            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            # 所有相关的destination
            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combination = db.session.query(Combination).filter(or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id), Combination.day3 == str(day_id), Combination.day4 == str(day_id), Combination.day5 == str(day_id), Combination.day6 == str(day_id), Combination.day7 == str(day_id))).all()

            return render_template("homepage2.html", Sets=combination)

    # 只搜索attractions
        elif (attraction is not None) and (destination == "") and (price_up == "") and (price_low == ""):
            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id1
                    combination = db.session.query(Combination).filter(or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id), Combination.day3 == str(day_id), Combination.day4 == str(day_id), Combination.day5 == str(day_id), Combination.day6 == str(day_id), Combination.day7 == str(day_id))).all()

            return render_template("homepage2.html", Sets=combination)

        # 只搜索价格最高区间
        elif (price_up is not None) and (destination == "") and (attraction == "") and (price_low == ""):
            # 查询在此价格往下的所有combination
            combination = db.session.query(Combination).filter(
                Combination.price <= str(price_up)).all()
            return render_template("homepage2.html", Sets=combination)

        # 只搜索价格最低的区间
        elif (price_low is not None) and (destination == "") and (attraction == "") and (price_up == ""):
            # 查询在此价格往下的所有combination
            combination = db.session.query(Combination).filter(
                Combination.price >= str(price_low)).all()
            return render_template("homepage2.html", Sets=combination)

        # 搜索价格最低的区间(上下)
        elif (price_low is not None) and (price_up is not None) and (attraction == "") and (destination == ""):
            # 查询在此价格往下的所有combination
            combination = db.session.query(Combination).filter((
                Combination.price >= str(price_low)), and_(Combination.price <= str(price_up))).all()
            return render_template("homepage2.html", Sets=combination)

        #搜索destination和attraction
        elif (destination is not None) and (attraction is not None) and (price_up == "") and (price_low == ""):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 模糊查询attractions

            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id
                    combinations2 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            #对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            print(combination)
            return render_template("homepage2.html", Sets=combination)

        #只搜索destination和price上区间
        elif (destination is not None) and (price_up is not None) and (attraction == "") and (price_low == ""):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations2 = db.session.query(Combination).filter(
                Combination.price <= str(price_up)).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            return render_template("homepage2.html", Sets=combination)

        # 只搜索destination和price下区间
        elif (destination is not None) and (price_low is not None) and (attraction == "") and (price_up == ""):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations2 = db.session.query(Combination).filter(
                Combination.price >= str(price_low)).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            return render_template("homepage2.html", Sets=combination)

        # 只搜索destination和price上下区间
        elif (destination is not None) and (price_low is not None) and (attraction == "") and (price_up is not None):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations2 = db.session.query(Combination).filter((
                    Combination.price >= str(price_low)), and_(Combination.price <= str(price_up))).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            return render_template("homepage2.html", Sets=combination)

        # 只搜索attraction和price上区间
        elif (attraction is not None) and (price_up is not None) and (destination == "") and (price_low == ""):

            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id1
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations2 = db.session.query(Combination).filter(
                Combination.price <= str(price_up)).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            return render_template("homepage2.html", Sets=combination)

        # 只搜索attraction和price下区间

        elif (attraction is not None) and (price_low is not None) and (destination == "") and (price_up == ""):

            # 模糊查询所有相关的attraction
            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id1
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations2 = db.session.query(Combination).filter(
                Combination.price >= str(price_low)).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            return render_template("homepage2.html", Sets=combination)

        # 只搜索attraction和price上下区间

        elif (attraction is not None) and (price_low is not None) and (destination == "") and (price_up is not None):

            # 模糊查询所有相关的attraction
            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id1
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations2 = db.session.query(Combination).filter((
                    Combination.price >= str(price_low)), and_(Combination.price <= str(price_up))).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2]
            return render_template("homepage2.html", Sets=combination)

        # 搜索destination和attraction和price上区间
        elif (attraction is not None) and (price_up is not None) and (destination is not None) and (price_low == ""):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id1
                    combinations2 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations3 = db.session.query(Combination).filter(
                Combination.price <= str(price_up)).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2 if combinations in combinations3]
            return render_template("homepage2.html", Sets=combination)

        # 搜索destination和attraction和price下区间

        elif (attraction is not None) and (price_low is not None) and (destination is not None) and (price_up == ""):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id1
                    combinations2 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations3 = db.session.query(Combination).filter(
                Combination.price >= str(price_low)).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2 if
                           combinations in combinations3]
            return render_template("homepage2.html", Sets=combination)

        # 搜索destination和attraction和price上下区间

        elif (attraction is not None) and (price_low is not None) and (destination is not None) and (price_up is not None):

            # 模糊查询地点
            destinations = db.session.query(Destination).filter(
                Destination.name.like("%" + destination + "%")).all()

            for destination in destinations:
                destination_id = destination.id
                # 与destination相关的day
                days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
                for day in days:
                    # 与day相关的combination
                    day_id = day.id
                    combinations1 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 模糊查询所有相关的attraction
            attractions = db.session.query(Target).filter(
                Target.name.like("%" + attraction + "%"), and_(Target.type == '0')).all()

            for attraction in attractions:
                attraction_id = attraction.id
                # 与attraction相关的day
                days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
                for day in days:
                    day_id = day.id
                    combinations2 = db.session.query(Combination).filter(
                        or_(Combination.day1 == str(day_id), Combination.day2 == str(day_id),
                            Combination.day3 == str(day_id), Combination.day4 == str(day_id),
                            Combination.day5 == str(day_id), Combination.day6 == str(day_id),
                            Combination.day7 == str(day_id))).all()

            # 查询在此价格往下的所有combination
            combinations3 = db.session.query(Combination).filter((
                    Combination.price >= str(price_low)), and_(Combination.price <= str(price_up))).all()

            # 对比两组数据中重复的数据
            combination = [combinations for combinations in combinations1 if combinations in combinations2 if
                           combinations in combinations3]
            return render_template("homepage2.html", Sets=combination)


        return render_template("homepage2.html", Sets=combination)












