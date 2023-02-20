import os

from flask import render_template, flash, redirect, url_for, request, session
from travelAgent import app

import logging
import random


logger = logging.getLogger(__name__)  # create a logger
logger.setLevel(logging.INFO)  # show messages above info level
fh = logging.FileHandler('travelAgent.log')  # log file handler
ch = logging.StreamHandler()  # input stream handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # set a formatter

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


@app.route("/")
@app.route("/index")
def index():
    # http://127.0.0.1:5000 return the home page
    logger.info('Entered the HOME page')
    return render_template("index.html")


if __name__ == '__main__':
    logger.info('The Website Starts Running!')
    app.run(debug=True, port=5001)