from travelAgent.models import User, Destination, Target, Day, Combination, Reply, ReplyC,Record, RecordC, CommentC, Comment, Collect, CollectC,EmailCaptchaModel
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

    des1 = Destination(id=1, name='Beijing')
    des2 = Destination(id=2, name='Tianjing')
    db.session.add_all([des1, des2])
    db.session.commit()

    # 暂定 0 为attraction，1 为accommodation， 2 为traffic
    tar1 = Target(id=1, name='故宫', destination_id=1, image='', intro='故宫的简介', type='0', price=20)
    tar2 = Target(id=2, name='家', destination_id=1, image='', intro='家的位置', type='1', price=100)
    tar3 = Target(id=3, name='公交车', destination_id=1, image='', intro='公交车的号码', type='2', price=2)
    tar4 = Target(id=4, name='长城', destination_id=1, image='', intro='长城的简介', type='0', price=10)
    tar5 = Target(id=5, name='酒店', destination_id=1, image='', intro='酒店的简介', type='1', price=300)
    tar6 = Target(id=6, name='地铁', destination_id=1, image='', intro='地铁的线路', type='2', price=6)
    db.session.add_all([tar1, tar2, tar3, tar4, tar5, tar6])
    db.session.commit()

    day1 = Day(id=1, destination_id=1, attraction_id=1, accommodation_id=2, traffic_id=3)
    day2 = Day(id=2, destination_id=1, attraction_id=4, accommodation_id=5, traffic_id=6)
    db.session.add_all([day1, day2])
    db.session.commit()

    com1 = Combination(id=1, name='test1——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test1_introduction', price=2000, length=7)
    com2 = Combination(id=2, name='test2——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test2_introduction', price=3000, length=7)
    com3 = Combination(id=3, name='test3——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test3_introduction', price=5000, length=7)
    com4 = Combination(id=4, name='test4——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test4_introduction', price=4000, length=7)
    db.session.add_all([com1, com2, com3, com4])
    db.session.commit()
