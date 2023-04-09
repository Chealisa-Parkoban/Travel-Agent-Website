import time

from travelAgent import app, db
from flask import Blueprint, render_template
from travelAgent.models import FavoriteC, Favorite, Combination, Target
from travelAgent.views.login_handler import current_user

favorite_blueprint = Blueprint(name="favorite", import_name=__name__)

# global Lc
# global Lt
# global La
# global Lh
# global Ltr

@favorite_blueprint.route('/favourites')
def showAll():
    Fc = FavoriteC.query.filter(FavoriteC.user_id == current_user.id).all()
    Ft = Favorite.query.filter(FavoriteC.user_id == current_user.id).all()
    Lc = []
    Lt = []
    La = []
    Lh = []  # accommodation
    Ltr = []

    for c in Fc:
        cID = c.combination_id
        combination = Combination.query.filter(Combination.id == cID).first()
        Lc.append(combination)

    # including 3 types:
    # attraction: 0,
    # accommodation: 1,
    # traffic: 2
    for t in Ft:
        tID = t.target_id
        target = Target.query.filter(Target.id == tID).first()
        attraction = Target.query.filter(Target.id == tID, Target.type == 0).first()
        accommodation = Target.query.filter(Target.id == tID, Target.type == 1).first()
        traffic = Target.query.filter(Target.id == tID, Target.type == 2).first()

        Lt.append(target)
        La.append(attraction)
        Lh.append(accommodation)
        Ltr.append(traffic)


    return render_template("favourites.html", Combinations=Lc, Targets=Lt, Attractions=La, Accommodations=Lh,
                           Traffics=Ltr)


@favorite_blueprint.route('/favourites/<combination_id>')
def addFavorite(combination_id):
    check = FavoriteC.query.filter(FavoriteC.user_id == current_user.id, FavoriteC.combination_id == combination_id).scalar() is None
    if check:

        f = FavoriteC(user_id=current_user.id, combination_id=combination_id, time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        db.session.add(f)
        db.session.commit()

    Fc = FavoriteC.query.filter(FavoriteC.user_id == current_user.id).all()
    Ft = Favorite.query.filter(FavoriteC.user_id == current_user.id).all()
    Lc = []
    Lt = []
    La = []
    Lh = []  # accommodation
    Ltr = []

    for c in Fc:
        cID = c.combination_id
        combination = Combination.query.filter(Combination.id == cID).first()
        Lc.append(combination)

    # including 3 types:
    # attraction: 0,
    # accommodation: 1,
    # traffic: 2
    for t in Ft:
        tID = t.target_id
        target = Target.query.filter(Target.id == tID).first()
        attraction = Target.query.filter(Target.id == tID, Target.type == 0).first()
        accommodation = Target.query.filter(Target.id == tID, Target.type == 1).first()
        traffic = Target.query.filter(Target.id == tID, Target.type == 2).first()

        Lt.append(target)
        La.append(attraction)
        Lh.append(accommodation)
        Ltr.append(traffic)
    return render_template("favourites.html", Combinations=Lc, Targets=Lt, Attractions=La, Accommodations=Lh,
                           Traffics=Ltr)