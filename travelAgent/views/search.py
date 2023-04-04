from flask import Blueprint

search_blueprint = Blueprint(name="travel_route_search", import_name=__name__)

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
from travelAgent.models import CommentC, Comment, Combination, Destination, Day, Target, RecordC
from travelAgent.views.login_handler import login_blueprint, current_user
from travelAgent.views.number import Random_str

# @search_blueprint.route("/search_for_route")
# def search():
#     search = request.form.get('')
