import random
import string
from datetime import datetime

import flask
from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, user_unauthorized
from flask_mail import Message
from flask_socketio import SocketIO

from .chatdatabase import DataBase

from travelAgent import app
from travelAgent.models import User, EmailCaptchaModel

socketio = SocketIO(app, cors_allowed_origins="*")
chat_blueprint = Blueprint(name="chat", import_name=__name__)


MSG_LIMIT = 100
logger = None


def set_logger(l):
    global logger
    logger = l


@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    """
    handles saving messages once received from web server
    and sending message to other clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    data = dict(json)
    if "username" in data:
        db = DataBase()
        db.save_message(data["username"], data["name"], data["message"])
        # record unseen
        if data['username'] == data['name']:
            cur_num = db.get_unseen(data['username'], False)
            db.set_unseen(data['username'], False, cur_num + 1)
        else:
            cur_num = db.get_unseen(data['username'], True)
            db.set_unseen(data['username'], True, cur_num + 1)
    else:
        logger.info(data['message'])
    socketio.emit('message response', json)


@chat_blueprint.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    # db = DataBase()
    # db.set_unseen(current_user.username, True, 0)
    return render_template('chat/chatindex.html', **{"current_user": current_user})


@chat_blueprint.route("/chat/history")
@login_required
def history():
    json_messages = get_history_of_user()
    print(json_messages)
    return render_template("chat/chathistory.html", **{"current_user": current_user, "history": json_messages})


@chat_blueprint.route("/chat/get_messages_of_user")
@login_required
def get_messages_of_user():
    """
    :return: all messages stored in database
    """
    db = DataBase()
    msgs = db.get_all_messages(MSG_LIMIT, current_user.username)
    # msgs = db.get_all_messages(1)  # 就只能显示倒数最后一条
    messages = remove_seconds_from_messages(msgs)  # 删除秒以后的精确时间位数，因为没必要
    return jsonify(messages)


@chat_blueprint.route("/chat/get_history_of_user")
@login_required
def get_history_of_user():
    """
    :return: all messages by name of user
    """
    username = request.args.get('username')
    db = DataBase()
    msgs = db.get_messages_by_username(username)
    messages = remove_seconds_from_messages(msgs)
    return messages


@chat_blueprint.route("/chat/all_user")
def get_all_user_with_unseen_admin():
    users = User.get_all()
    res = []
    db = DataBase()
    for u in users:
        if u.isAdmin():
            continue
        num = db.get_unseen(u.username, False)
        res.append({"username": u.username, "unseen": num})
    return jsonify(res)


@chat_blueprint.route("/chat/adminname")
def admin_name():
    return jsonify({'adminname': current_user.username})


@chat_blueprint.route("/chat/unseen")
def get_unseen_user():
    db = DataBase()
    num = db.get_unseen(current_user.username, True)
    return jsonify({'unseen': num})


@chat_blueprint.route("/chat/unseen/reset")
def reset_unseen_user():
    db = DataBase()
    db.set_unseen(current_user.username, True, 0)
    return jsonify()


@chat_blueprint.route("/chat/unseen/reset/admin")
def reset_unseen_admin():
    username = request.args['username']
    db = DataBase()
    db.set_unseen(username, False, 0)
    return jsonify()


# UTILITIES
def remove_seconds_from_messages(msgs):
    """
    removes the seconds from all messages
    :param msgs: list
    :return: list
    """
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = remove_seconds(message["time"])
        messages.append(message)

    return messages


def remove_seconds(msg):
    """
    :return: string with seconds trimmed off
    """
    return msg.split(".")[0][:-3]