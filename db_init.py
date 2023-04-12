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
    des2 = Destination(id=2, name='Shanghai')
    des3 = Destination(id=3, name='New York')
    des4 = Destination(id=4, name='Dublin')
    des5 = Destination(id=5, name='Paris')
    des6 = Destination(id=6, name='London')
    db.session.add_all([des1, des2, des3, des4, des5, des6])
    db.session.commit()

    # 暂定 0 为attraction，1 为accommodation， 2 为traffic
    # ---------------------------accommodations--------------------------------

    # New York
    acc1 = Target(name='Royalton New York', destination_id=3, image='static/upload/royalton.png', intro='This New York City hotel is located on 44th Street and is 1056 feet from Times Square. It features guest rooms with flat-screen TVs.', type='1', price=2310)
    acc2 = Target(name='Hyatt Place Times Square', destination_id=3, image='static/upload/Hyatt.png', intro="Hyatt Place New York City/Times Square features air-conditioned rooms with satellite flat-screen TV in the Hell's Kitchen district of New York City.", type='1', price=1990)
    acc3 = Target(name='Iroquois New York', destination_id=3, image='static/upload/iro.png', intro='49 West 44th Street, New York, NY 10036, United States of America – Subway Access', type='1', price=2610)
    acc4 = Target(name='Dylan Hotel NYC', destination_id=3, image='static/upload/dylan.png', intro='52 East 41st Street, Murray Hill, New York, NY 10017, United States of America – Subway Access', type='1', price=1890)

    # Dublin
    acc5 = Target(name='Blooms Hotel', destination_id=4, image='static/upload/Blooms.png', intro='Blooms Hotel', type='1', price=539)
    acc6 = Target(name='The Spencer Hotel', destination_id=4, image='static/upload/Spencer.png', intro='The Spencer Hotel', type='1', price=786)
    acc7 = Target(name='The Shelbourne', destination_id=4, image='static/upload/Shelbourne.png', intro='The Shelbourne, Autograph Collection', type='1', price=1343)

    # ---------------------------attractions--------------------------------
    # New York
    att1 = Target(name='SUMMIT One Vanderbilt', destination_id=3, image='static/upload/SUMMIT2.png', intro='Digital art installations and views of New York from a skyscraper terrace', type='0', price=130)
    att2 = Target(name='Statue of Liberty', destination_id=3, image='static/upload/Liberty.png', intro='A chance to get up close to the Statue of Liberty during a 50-minute cruise', type='0', price=230)
    att3 = Target(name='9/11 Memorial & Museum', destination_id=3, image='static/upload/911.png', intro="You’ll visit the 9/11 Memorial and have a chance to learn more about the September 11 attacks", type='0', price=30)
    att4 = Target(name='Broadway | Lion King', destination_id=3, image='static/upload/Broadway.png', intro='A chance to watch a musical theater performance in New York', type='0', price=1456)

    # Dublin
    att5 = Target(name='Cliffs of Moher and Galway', destination_id=4, image='static/upload/Galway.png', intro='Day trip along the Wild Atlantic Way to see the famous cliffs and explore Galway', type='0', price=356)
    att6 = Target(name='Jameson Distillery Tour', destination_id=4, image='static/images/sample_pic/the_north_Europe.png', intro='Ticket for guided immersive tour of Jameson Distillery with whiskey tasting', type='0', price=256)
    att7 = Target(name='Hop-On Hop-Off Tour', destination_id=4, image='static/upload/Hop.png', intro='A chance to explore Dublin on a hop-on hop-off bus tour', type='0', price=180)
    att8 = Target(name='Blarney Castle', destination_id=4, image='static/upload/Blarney.png', intro="Blarney Castle, Rock of Cashel and Cork Tour. A full-day tour of some of Ireland's most famous landmarks", type='0', price=210)

    # ---------------------------traffic--------------------------------
    tra1 = Target( name='Bus', destination_id=1, image='static/upload/bus.png', intro='Please see the details page for specific routes', type='2', price=2)
    tra2 = Target( name='Subway', destination_id=1, image='static/upload/subway.png', intro='Please see the details page for specific routes', type='2', price=6)
    tra3 = Target( name='Taxi', destination_id=1, image='static/upload/taxi.png', intro='Please see the details page for specific routes', type='2', price=10)
    tra4 = Target( name='flight', destination_id=1, image='static/upload/flight.png', intro='Please see the details page for specific routes', type='2', price=1000)
    tra5 = Target( name='On foot', destination_id=1, image='static/upload/.png', intro='Please see the details page for specific routes', type='2', price=0)

    # tar3 = Target( name='Bus', destination_id=1, image='', intro='公交车的号码', type='2', price=2)
    # tar4 = Target( name='The Great Wall', destination_id=1, image='', intro='长城的简介', type='0', price=10)
    # tar5 = Target( name='Green Tree Inn', destination_id=2, image='', intro='格林豪泰大酒店', type='1', price=300)
    #
    # tar6 = Target( name='地铁', destination_id=1, image='', intro='地铁的线路', type='2', price=6)
    # tar7 = Target( name='八达岭', destination_id=1, image='', intro='香山八达岭', type='0', price=6)
    # tar8 = Target( name='环球影城', destination_id=1, image='', intro='北京环球影城度假区', type='0', price=330)
    #
    # tar9 = Target( name='飞机', destination_id=1, image='', intro='波音737-800', type='2', price=2200)
    # tar10 = Target( name='打车', destination_id=1, image='', intro='嘀嘀打车', type='2', price=40)
    #
    # tar11 = Target( name='希尔顿', destination_id=3, image='', intro='上海希尔顿酒店', type='1', price=1200)
    # tar12 = Target( name='丽思卡尔顿', destination_id=1, image='', intro='北京丽思卡尔顿大酒店', type='1', price=3000)
    # tar13 = Target( name='上海迪士尼乐园', destination_id=3, image='', intro='上海迪士尼度假区 Disney Resort', type='0', price=543)

    db.session.add_all([acc1, acc2, acc3, acc4, acc5, acc6, acc7, att1, att2, att3, att4, att5, att6, att7, att8, tra1,
                        tra2, tra3, tra4, tra5])
    db.session.commit()

    # ---------------------------com1--------------------------------#
    day1 = Day(id=1, destination_id=3, attraction_id=9, accommodation_id=1, traffic_id=17)
    day2 = Day(id=2, destination_id=3, attraction_id=8, accommodation_id=1, traffic_id=18)  # abandon
    day3 = Day(id=3, destination_id=3, attraction_id=10, accommodation_id=4, traffic_id=20)

    # ---------------------------com2--------------------------------#
    day4 = Day(id=4, destination_id=3, attraction_id=9, accommodation_id=1, traffic_id=17)
    day5 = Day(id=5, destination_id=3, attraction_id=8, accommodation_id=1, traffic_id=18)
    day6 = Day(id=6, destination_id=3, attraction_id=10, accommodation_id=4, traffic_id=20)
    day7 = Day(id=7, destination_id=3, attraction_id=11, accommodation_id=1, traffic_id=16)

    # ---------------------------com3--------------------------------#
    day8 = Day(id=8, destination_id=4, attraction_id=12, accommodation_id=5, traffic_id=18)
    day9 = Day(id=9, destination_id=4, attraction_id=13, accommodation_id=6, traffic_id=18)
    day10 = Day(id=10, destination_id=4, attraction_id=14, accommodation_id=6, traffic_id=16)
    day11 = Day(id=11, destination_id=4, attraction_id=15, accommodation_id=7, traffic_id=17)


    db.session.add_all([day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11])
    db.session.commit()

    com1 = Combination(name="New York Two-Day Trip", day1=1, day2=3, day3=None, day4=None, day5=None, day6=None, day7=None,
                       intro='New York Four-Day Trip', price=3350, length=2, image='static/upload/Liberty.png')
    com2 = Combination(name='New York Four-Day Trip', day1=4, day2=5, day3=6, day4=7, day5=None, day6=None, day7=None,
                       intro='test2_introduction', price=5250, length=4, image='static/upload/summit2.png')
    com3 = Combination(name='Dublin Four-Day Trip', day1=8, day2=9, day3=10, day4=11, day5=None, day6=None, day7=None,
                          intro='test3_introduction', price=4250, length=4, image='static/upload/Galway.png')

    db.session.add_all([com1, com2, com3])
    db.session.commit()
