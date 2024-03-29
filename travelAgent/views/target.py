import requests
from flask import Blueprint

# from travelAgent.app import logger
from travelAgent.config import basedir

target_blueprint = Blueprint(name="targets", import_name=__name__)

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
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, Record, Favorite, User
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str


@target_blueprint.route("/showAttraction", methods=['GET', 'POST'])
def showAttraction():
    # receive id from front end
    set_id = session.get("set_id")
    print(set_id)
    target_id = set_id

    set = db.session.query(Target).filter(Target.id == set_id).first()

    comment_form = CommentForm(request.form)
    id = Random_str().create_uuid()
    status_fav = True

    if current_user.is_authenticated:
        Ft = Favorite.query.filter(Favorite.user_id == current_user.id, Favorite.target_id == target_id).first()
    # default status: true, not favorite
        if Ft is not None:
            # false, can be cancel favorite
            status_fav = False

    if request.method == 'POST':

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

            record = Record.query.filter(Record.target_id == set_id, Record.user_id == current_user.id).first()
            comment_check = True
            if record is not None:
                if record.status == "Uncompleted":
                    comment_check = False
                    flash("You have not completed this order yet and cannot comment")
                    # return redirect(url_for("showAttraction"))
                for comment in Comment.query.filter(Comment.target_id == set_id,
                                                    Comment.user_id == current_user.id).all():
                    if comment.content == comment_form.comment.data:
                        comment_check = False
                        flash("You have already commented on the same content")
                        break

                if comment_check:
                    comment = Comment(user_id=current_user.id, username=current_user.get_username(), target_id=target_id,
                                      score=comment_form.score.data, content=comment_form.comment.data, image=path,
                                      time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    record.status2 = "Commented"
                    db.session.add(comment)
                    db.session.commit()

            else:
                flash("You have not booked this order yet and cannot comment")

        comment_users = []
        comments = db.session.query(Comment).filter(Comment.target_id == set_id).all()
        for comment in comments:
            user_id = comment.user_id
            comment_user = User.query.filter(User.id == user_id).first()
            comment_users.append(comment_user)

        return render_template("attractionDetail.html", current_user=current_user, comment_form=comment_form,
                               comments=db.session.query(Comment).filter(Comment.target_id == set_id).all(), set=set,
                               target_id=target_id, status_fav=status_fav, comment_users=comment_users
                               )

    # if request.method == 'GET':
    comment_users = []
    comments = db.session.query(Comment).filter(Comment.target_id == set_id).all()
    for comment in comments:
        user_id = comment.user_id
        comment_user = User.query.filter(User.id == user_id).first()
        comment_users.append(comment_user)


    return render_template("attractionDetail.html", comments=comments, comment_form=comment_form,
                           set=set, target_id=target_id, status_fav=status_fav, comment_users=comment_users)
