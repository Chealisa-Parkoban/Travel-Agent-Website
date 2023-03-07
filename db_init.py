from travelAgent.models import User, Staff, Destination, Attraction, Accommodation, Traffic, Type, Atom, Booking, \
    Comment
from travelAgent import db
from travelAgent import app

with app.app_context():
    db.drop_all()  # delete tables exists
    db.create_all()  # create all tables

    us1 = User(username='wang', email='wang@163.com')
    db.session.add_all([us1])
    db.session.commit()