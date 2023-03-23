from flask import Blueprint, render_template
from flask_login import LoginManager

from travelAgent import app

background_blueprint = Blueprint(name="staff_site", import_name=__name__)


@background_blueprint.route('/staff', methods=['GET', 'POST'])
def staff():
    return render_template('./staff_site/pages/samples/login.html')


@background_blueprint.route('/staff/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('./background/dashboard.html')