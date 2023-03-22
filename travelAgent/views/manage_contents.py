from flask import Blueprint, render_template
from flask_login import LoginManager

from travelAgent import app

content_blueprint = Blueprint(name="contents", import_name=__name__)


@content_blueprint.route('/admin/contents', methods=['GET', 'POST'])
def contents():
    return render_template('./background/contents.html')