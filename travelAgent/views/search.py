from flask import Blueprint
from flask_sqlalchemy import session
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

import travelAgent
from travelAgent import db
from travelAgent import app
from travelAgent.forms import CommentForm, ImageForm
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, RecordC
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str

@search_blueprint.route("/search_for_route", methods=['GET', 'POST'])
def search():
    destination = request.form.get('Destination')
    attraction = request.form.get('Attraction')
    price_up = request.form.get('Highest')
    price_low = request.form.get('Lowest')
    print(destination)
    print(attraction)
    print(price_up)
    print(price_low)


    # 只搜索combination
    if (destination is not None) and (attraction is None) and (price_up is None) and (price_low is None):
        # destination = db.session.query(Destination).filter(Destination.name == destination).first()
        # 模糊查询
        sql1 = "SELECT * from Combination where name like concat( '%' ,denstination, '%' );"
        # 所有相关的destination
        destinations = session.execute(text(sql1))
        for destination in destinations:
            destination_id = destination.id
            # 与destination相关的day
            days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
            for day in days:
                # 与day相关的combination
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2="+ day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id +";"
                combinations = session.execute(text(sql2))


# 只搜索attractions
    elif (attraction is not None) and (destination is None) and (price_up is None) and (price_low is None):
        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations = session.execute(text(sql2))

    # 只搜索价格最高区间
    elif (price_up is not None) and (destination is None) and (attraction is None) and (price_low is None):
        # 查询在此价格往下的所有combination
        sql1 = "select * from Combination where price between 0 and " + price_up + ";"
        combinations = session.execute(text(sql1))

    # 只搜索价格最低的区间
    elif (price_low is not None) and (destination is None) and (attraction is None) and (price_up is None):
        # 查询在此价格往下的所有combination
        sql1 = "select * from Combination where price between " + price_low + " and 9999999999999999999999";
        combinations = session.execute(text(sql1))

    # 搜索价格最低的区间(上下)
    elif (price_low is not None) and (price_up is not None) and (attraction is None) and (destination is None):
        # 查询在此价格往下的所有combination
        sql1 = "select * from Combination where price between " + price_low + " and "+ price_up + ";"
        combinations = session.execute(text(sql1))

    #搜索destination和attraction
    elif (destination is not None) and (attraction is not None) and (price_up is None) and (price_low is None):

        # 模糊查询地点
        sql1 = "SELECT * from Combination where name like concat( '%' ,denstination, '%' );"
        destinations = session.execute(text(sql1))
        # 所有相关的destination
        destinations = session.execute(text(sql1))
        for destination in destinations:
            destination_id = destination.id
            # 与destination相关的day
            days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
            for day in days:
                # 与day相关的combination
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 模糊查询attractions
        sql3 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql3))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql4 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations2 = session.execute(text(sql4))

        #对比两组数据中重复的数据
        sql5 = "select * from  "+ combinations1 +" inner join "+ combinations2 +" on " + combinations1 +".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql5))

    #只搜索destination和price上区间
    elif (destination is not None) and (price_up is not None) and (attraction is None) and (price_low is None):

        # 模糊查询地点
        sql1 = "SELECT * from Combination where name like concat( '%' ,denstination, '%' );"
        destinations = session.execute(text(sql1))
        # 所有相关的destination
        destinations = session.execute(text(sql1))
        for destination in destinations:
            destination_id = destination.id
            # 与destination相关的day
            days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
            for day in days:
                # 与day相关的combination
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 查询在此价格往下的所有combination
        sql3 = "select * from Combination where price between 0 and " + price_up + ";"
        combinations2 = session.execute(text(sql3))

        # 对比两组数据中重复的数据
        sql4 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql4))



    # 只搜索destination和price下区间
    elif (destination is not None) and (price_low is not None) and (attraction is None) and (price_up is None):

        # 模糊查询地点
        sql1 = "SELECT * from Combination where name like concat( '%' ,denstination, '%' );"
        destinations = session.execute(text(sql1))
        # 所有相关的destination
        destinations = session.execute(text(sql1))
        for destination in destinations:
            destination_id = destination.id
            # 与destination相关的day
            days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
            for day in days:
                # 与day相关的combination
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 查询在此价格往下的所有combination
        sql3 = "select * from Combination where price between " + price_low + " and 9999999999999999999999";
        combinations2 = session.execute(text(sql3))

        # 对比两组数据中重复的数据
        sql4 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql4))

    # 只搜索destination和price上下区间

    elif (destination is not None) and (price_low is not None) and (attraction is None) and (price_up is not None):

        # 模糊查询地点
        sql1 = "SELECT * from Combination where name like concat( '%' ,denstination, '%' );"
        destinations = session.execute(text(sql1))
        # 所有相关的destination
        destinations = session.execute(text(sql1))
        for destination in destinations:
            destination_id = destination.id
            # 与destination相关的day
            days = db.session.query(Day).filter(Day.destination_id == destination_id).all()
            for day in days:
                # 与day相关的combination
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 查询在此价格往下的所有combination
        sql3 = "select * from Combination where price between " + price_low + " and "+ price_up + ";"
        combinations2 = session.execute(text(sql3))

        # 对比两组数据中重复的数据
        sql4 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql4))



    # 只搜索attraction和price上区间
    elif (attraction is not None) and (price_up is not None) and (destination is None) and (price_low is None):

        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 查询在此价格往下的所有combination
        sql3 = "select * from Combination where price between 0 and " + price_up + ";"
        combinations2 = session.execute(text(sql3))

        # 对比两组数据中重复的数据
        sql4 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql4))


    # 只搜索attraction和price下区间

    elif (attraction is not None) and (price_low is not None) and (destination is None) and (price_up is None):

        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 查询在此价格往下的所有combination
        sql3 = "select * from Combination where price between " + price_low + " and 9999999999999999999999";
        combinations2 = session.execute(text(sql3))

        # 对比两组数据中重复的数据
        sql4 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql4))

    # 只搜索attraction和price上下区间

    elif (attraction is not None) and (price_low is not None) and (destination is None) and (price_up is  not None):

        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 查询在此价格往下的所有combination
        sql3 = "select * from Combination where price between " + price_low + " and "+ price_up + ";"
        combinations2 = session.execute(text(sql3))

        # 对比两组数据中重复的数据
        sql4 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination = session.execute(text(sql4))

    # 搜索destination和attraction和price上区间
    elif (attraction is not None) and (price_up is not None) and (destination is not None) and (price_low is None):

        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 模糊查询所有相关的attraction
        sql3 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql3))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql4 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations2 = session.execute(text(sql4))


        # 查询在此价格往下的所有combination
        sql5 = "select * from Combination where price between 0 and " + price_up + ";"
        combinations3 = session.execute(text(sql5))


        # 对比两组数据中重复的数据
        sql6 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination_12 = session.execute(text(sql6))

        sql7 = "select * from  " + combination_12 + " inner join " + combinations3 + " on " + combination_12 + ".id=" + combinations3 + ".id;"
        combination = session.execute(text(sql7))



    # 搜索destination和attraction和price下区间

    elif (attraction is not None) and (price_low is not None) and (destination is not None) and (price_up is None):

        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 模糊查询所有相关的attraction
        sql3 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql3))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql4 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations2 = session.execute(text(sql4))


        # 查询在此价格往下的所有combination
        sql5 = "select * from Combination where price between " + price_low + " and 9999999999999999999999";
        combinations3 = session.execute(text(sql5))


        # 对比两组数据中重复的数据
        sql6 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination_12 = session.execute(text(sql6))

        sql7 = "select * from  " + combination_12 + " inner join " + combinations3 + " on " + combination_12 + ".id=" + combinations3 + ".id;"
        combination = session.execute(text(sql7))

    # 搜索destination和attraction和price上下区间

    elif (attraction is not None) and (price_low is not None) and (destination is not None) and (price_up is not None):

        # 模糊查询所有相关的attraction
        sql1 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql1))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql2 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations1 = session.execute(text(sql2))

        # 模糊查询所有相关的attraction
        sql3 = "SELECT * from Target where type=1 and like  concat( '%' ,attraction, '%' );"
        attractions = session.execute(text(sql3))
        for attraction in attractions:
            attraction_id = attraction.id
            # 与attraction相关的day
            days = db.session.query(Day).filter(Day.attraction_id == attraction_id).all()
            for day in days:
                day_id = day.id
                sql4 = "select * from Combination where day1=" + day_id + " or day2=" + day_id + " or day3=" + day_id + " or day4=" + day_id + " or day5=" + day_id + " or day6=" + day_id + " or day7=" + day_id + ";"
                combinations2 = session.execute(text(sql4))


        # 查询在此价格往下的所有combination
        sql5 ="select * from Combination where price between " + price_low + " and "+ price_up + ";"
        combinations3 = session.execute(text(sql5))


        # 对比两组数据中重复的数据
        sql6 = "select * from  " + combinations1 + " inner join " + combinations2 + " on " + combinations1 + ".id=" + combinations2 + ".id;"
        combination_12 = session.execute(text(sql6))

        sql7 = "select * from  " + combination_12 + " inner join " + combinations3 + " on " + combination_12 + ".id=" + combinations3 + ".id;"
        combination = session.execute(text(sql7))


    return render_template("homepage2.html", combinations=combination)









