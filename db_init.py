from travelAgent.models import User, Destination, Target, Day, Combination, Reply, ReplyC,Record, RecordC, CommentC, Comment, FavoriteC, Favorite,EmailCaptchaModel
# from travelAgent.models import User
from travelAgent import db
from travelAgent import app

with app.app_context():
    db.drop_all()  # delete tables exists
    db.create_all() # create all tables

    us1 = User(username='staff1', email='staff1@163.com', password='123456', is_admin=1)
    us2 = User(username='staff2', email='staff2@163.com', password='123456', is_admin=1)
    us3 = User(username='selina', email='selina@163.com', password='1111', is_admin=0)
    us4 = User(username='allen', email='allen@ucd.ie', password='1225', is_admin=0)
    db.session.add_all([us1, us2, us3, us4])
    db.session.commit()

    des1 = Destination(id=1, name='Beijing')
    des2 = Destination(id=2, name='Tianjin')
    des3 = Destination(id=3, name='Shanghai')
    des4 = Destination(id=3, name='Xiamen')
    db.session.add_all([des1, des2, des3])
    db.session.commit()

    # 暂定 0 为attraction，1 为accommodation， 2 为traffic
    tar1 = Target( name='Summer Palace', destination_id=1, image='', intro='故宫的简介', type='0', price=0)
    tar2 = Target( name='家', destination_id=1, image='', intro='家的位置', type='1', price=100)
    tar3 = Target( name='Bus', destination_id=1, image='', intro='公交车的号码', type='2', price=2)
    tar4 = Target( name='The Great Wall', destination_id=1, image='', intro='长城的简介', type='0', price=10)
    tar5 = Target( name='Green Tree Inn', destination_id=2, image='', intro='格林豪泰大酒店', type='1', price=300)

    tar6 = Target( name='地铁', destination_id=1, image='', intro='地铁的线路', type='2', price=6)
    tar7 = Target( name='八达岭', destination_id=1, image='', intro='香山八达岭', type='0', price=6)
    tar8 = Target( name='环球影城', destination_id=1, image='', intro='北京环球影城度假区', type='0', price=330)

    tar9 = Target( name='飞机', destination_id=1, image='', intro='波音737-800', type='2', price=2200)
    tar10 = Target( name='打车', destination_id=1, image='', intro='嘀嘀打车', type='2', price=40)

    tar11 = Target( name='希尔顿', destination_id=3, image='', intro='上海希尔顿酒店', type='1', price=1200)
    tar12 = Target( name='丽思卡尔顿', destination_id=1, image='', intro='北京丽思卡尔顿大酒店', type='1', price=3000)
    tar13 = Target( name='上海迪士尼乐园', destination_id=3, image='', intro='上海迪士尼度假区 Disney Resort', type='0', price=543)

    db.session.add_all([tar1, tar2, tar3, tar4, tar5, tar6, tar7, tar8, tar9, tar10, tar11, tar12, tar13])
    db.session.commit()

    day1 = Day(id=1, destination_id=1, attraction_id=1, accommodation_id=2, traffic_id=3)
    day2 = Day(id=2, destination_id=1, attraction_id=4, accommodation_id=5, traffic_id=6)
    db.session.add_all([day1, day2])
    db.session.commit()

    com1 = Combination(name='test1——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test1_introduction', price=2000, length=7, image='')
    com2 = Combination(name='test2——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test2_introduction', price=3000, length=7, image='')
    com3 = Combination(name='test3——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test3_introduction', price=5000, length=7, image='')
    com4 = Combination(name='test4——Combination', day1=1, day2=1, day3=2, day4=2, day5=2, day6=1, day7=2,
                       intro='test4_introduction', price=4000, length=7, image='')
    db.session.add_all([com1, com2, com3, com4])
    db.session.commit()
