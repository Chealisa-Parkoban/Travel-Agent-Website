import os
from flask import Flask, render_template
import logging

from travelAgent import db
from travelAgent import app
from travelAgent.views.login_handler import login_blueprint

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
    return render_template("index.html")


@app.route('/about')
def about():
    logger.info('Entered the ABOUT page')
    return render_template("about.html")


@app.route('/contactUs')
def contact_us():
    logger.info('Entered the CONTACT page')
    return render_template("contact.html")

@app.route('/homepage')
def homepage():
    logger.info('Entered the HOME page')
    return render_template("homepage.html")


if __name__ == '__main__':
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5000)
