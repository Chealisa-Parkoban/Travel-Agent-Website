from travelAgent.models import User, SimpleComment, Staff, Destination, Attraction, Accommodation, Traffic, Type, Day, Combination, ReplyA, ReplyC, ReplyH, RecordA, RecordC, RecordH, RecordT, CommentC, CommentA, CommentH, EmailCaptchaModel
# from travelAgent.models import User
from travelAgent import db
from travelAgent import app

with app.app_context():
    db.drop_all()  # delete tables exists
    db.create_all() # create all tables

    us1 = User(username='staff1', email='staff1@163.com', password='123456', is_admin=1)
    us2 = User(username='staff2', email='staff2@163.com', password='123456', is_admin=1)
    us3 = User(username='selina', email='selina@163.com', password='1111', is_admin=0)
    db.session.add_all([us1, us2, us3])
    db.session.commit()