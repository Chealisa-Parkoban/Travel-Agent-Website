import random
import string
from datetime import datetime

import flask
from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_mail import Message

from travelAgent import app, db, mail
from travelAgent.forms import LoginForm, SignupForm

from travelAgent.models import User, EmailCaptchaModel

login_manager = LoginManager()
login_manager.init_app(app)


login_blueprint = Blueprint(name="account", import_name=__name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user, 'login')
    print(current_user._get_current_object(), 'login2')

    global emsg
    app.logger.info('Entered LOGIN page')
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
    # if True:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.get_by_username(username)
            if user is None:
                emsg = "Username not exist!"
            else:
                if user.verify_password(password):
                    login_user(user)

                    print(current_user, 'loginin')

                    emsg = "Login successfully!"
                    app.logger.info('User \'' + username + '\' has successfully logged into the website')
                    return redirect(url_for("account.login"))
                else:
                    emsg = "Wrong password!"

        return render_template('login.html', form=form, message=emsg)

            # for u in users:
                # if username-password pair exists in the database, login successfully
                # if u.username == username and check_password_hash(u.password_hash, password):
                    # login_user(my_user(u.username, u.password_hash, u.id))
                    # print(type(u))
                    # login_user(u)
                    # print(u.is_authenticated, 'login')
                    # app.logger.info('User \'' + u.username + '\' has successfully logged into the website')
                    # return redirect(url_for("index"))

            # app.logger.error('Login failed: Wrong username or password')
            # return render_template('login.html', form=form, message='Wrong username or password!')
        # return render_template('login.html', form=form)


@login_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    app.logger.info('The user has logged out')
    return redirect(url_for("index"))


@login_blueprint.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    app.logger.info('Entered SIGN UP page')

    form = SignupForm(request.form)

    if request.method == 'GET':
        return render_template('sign_up.html', title='sign_up', form=form)
    else:
        if form.validate_on_submit():
            app.logger.info('Sign up form information get')
            # get user's information
            newname = form.username.data
            email = form.email.data
            # captcha = form.email_verification_code.data
            password = form.password.data

            # session['userExist'] = 'false'
            # store user's information into database
            u1 = User(newname, email, password)
            db.session.add(u1)
            db.session.commit()
            app.logger.info('User \'' + newname + '\' has successfully signed up')

            # flash the message
            flash('Signup requested for user {}'.format(form.username.data))
            # redirect to the login page, for user to login
            return redirect(url_for("account.login"))
        else:
            app.logger.error('Sign up information not valid.')

    return render_template('sign_up.html', title='sign-up', form=form)


@login_blueprint.route("/captcha", methods=['POST'])
def get_captcha():
    # GET, POST
    email = request.form.get("email")
    # captcha_source = string.ascii_letters + string.digits
    captcha_source = string.digits
    captcha = "".join(random.sample(captcha_source, 6))
    if email:
        message = Message(
            subject="【Digital Beans】Verification Code",
            recipients=[email],
            body=f"【Digital Beans】Your verification code：{captcha}。Please do not tell anyone else！",
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha: ", captcha)
        # code:200 成功的、正常的请求
        return jsonify({"code": 200})
    else:
        # code: 40 客户端错误
        return jsonify({"code": 400, "message": "请先传递邮箱"})


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)