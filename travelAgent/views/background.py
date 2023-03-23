from flask import Blueprint, render_template
from flask_login import LoginManager

from travelAgent import app

background_blueprint = Blueprint(name="background", import_name=__name__)


@background_blueprint.route('/admin/contents', methods=['GET', 'POST'])
def contents():
    return render_template('./background/contents.html')


@background_blueprint.route('/admin/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('./background/dashboard.html')