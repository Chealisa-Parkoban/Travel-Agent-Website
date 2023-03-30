from travelAgent import app, db
from flask import Blueprint

favorite_blueprint = Blueprint(name="favorite", import_name=__name__)

# @favorite_blueprint.route('/favourites', methods=['GET', 'POST'])
# def showAll():
