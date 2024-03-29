from travelAgent.models import User, Destination, Target, Day, Combination, UserCombination, Reply, ReplyC,Record, RecordC, CommentC, Comment, FavoriteC, Favorite,EmailCaptchaModel, ContactModel
# from travelAgent.models import User
from travelAgent import db
from travelAgent import app

with app.app_context():
    db.drop_all()  # delete tables exists
    db.create_all() # create all tables

    us1 = User(username='staff1', email='staff1@163.com', password='staff_test123', is_admin=1)
    us2 = User(username='staff2', email='staff2@163.com', password='123456', is_admin=1)
    us3 = User(username='Selina', email='selina@163.com', password='user_test!123', is_admin=0)
    us4 = User(username='allen', email='allen@ucd.ie', password='1225', is_admin=0)
    us5 = User(username='chiquita', email='chiquita@ucd.ie', password='2222', is_admin=0)
    us6 = User(username='Lily', email='Lily@ucd.ie', password='1111', is_admin=0)
    us7 = User(username='Jenny', email='Jenny@ucd.ie', password='1111', is_admin=0)
    db.session.add_all([us1, us2, us3, us4, us5, us6, us7])
    db.session.commit()

    des1 = Destination(id=1, name='Beijing')
    des2 = Destination(id=2, name='Shanghai')
    des3 = Destination(id=3, name='New York')
    des4 = Destination(id=4, name='Dublin')
    des5 = Destination(id=5, name='Paris')
    des6 = Destination(id=6, name='London')
    des7 = Destination(id=7, name='Chengdu')
    des8 = Destination(id=8, name='Sydney')
    des9 = Destination(id=9, name='Copenhagen')
    des10 = Destination(id=10, name='Roma')
    des11 = Destination(id=11, name='Florence')
    db.session.add_all([des1, des2, des3, des4, des5, des6,des7,des8,des9,des10,des11])
    db.session.commit()

    # 暂定 0 为attraction，1 为accommodation， 2 为traffic
    # ---------------------------accommodations--------------------------------

    # New York
    acc1 = Target(name='Royalton New York', destination_id=3, image='static/upload/royalton.png', intro='This New York City hotel is located on 44th Street and is 1056 feet from Times Square. It features guest rooms with flat-screen TVs.', type='1', price=2310)
    acc2 = Target(name='Hyatt Place Times Square', destination_id=3, image='static/upload/Hyatt.png', intro="Hyatt Place New York City/Times Square features air-conditioned rooms with satellite flat-screen TV in the Hell's Kitchen district of New York City.", type='1', price=1990)
    acc3 = Target(name='Iroquois New York', destination_id=3, image='static/upload/iro.png', intro='49 West 44th Street, New York, NY 10036, United States of America – Subway Access', type='1', price=2610)
    acc4 = Target(name='Dylan Hotel NYC', destination_id=3, image='static/upload/dylan.png', intro='52 East 41st Street, Murray Hill, New York, NY 10017, United States of America – Subway Access', type='1', price=1890)

    # Dublin
    acc5 = Target(name='Blooms Hotel', destination_id=4, image='static/upload/Blooms.png', intro='Blooms Hotel is located in Dublin’s Temple Bar district, 492 feet from Trinity College and Dublin Castle. It has a traditional Irish pub, a nightclub and rooms with flat-screen TVs.', type='1', price=539)
    acc6 = Target(name='The Spencer Hotel', destination_id=4, image='static/upload/Spencer.png', intro="Overlooking the River Liffey, The Spencer Hotel is 10 minutes from the famous O'Connell Bridge and 20 minutes from the Temple Bar and Grafton Street.", type='1', price=786)
    acc7 = Target(name='The Shelbourne', destination_id=4, image='static/upload/Shelbourne.png', intro='The Shelbourne, Autograph Collection', type='1', price=1343)

    # Beijing
    acc8 = Target(name='Waldorf Astoria Beijing', destination_id=1, image='static/upload/waldorf.jpg',
                  intro='Expansive and contemporary with a Chinese flavour, rooms. Located at No.5-15, Jingyu Hutong, Dongcheng District, Beijin. ', type='1', price=2888)
    acc9 = Target(name='Tianlun Dynasty Hotel', destination_id=1, image='static/upload/tianlun.jpg',
                  intro='Ideally located in the heart of the bustling Wangfujing Commercial Area, Sunworld Dynasty Hotel Beijing is surrounded by plenty of popular shopping malls and stylish restaurants.', type='1', price=960)

    # Shanghai
    acc10 = Target(name='Hotel Equatorial', destination_id=2, image='static/upload/equatorial.jpg', intro='Hotel Equatorial Shanghai is conveniently situated about a 4-minute drive from Shanghai Exhibition Centre and Nanjing Road shopping street. ', type='1', price=1600)

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

    # Beijing
    att9 = Target(name='Forbidden City-The Palace Museum', destination_id=1, image='static/upload/forbidden.jpg', intro='The Forbidden City in Beijing is a royal palace of the Ming and Qing dynasties of China, formerly known as the Forbidden City.', type='0', price=60)
    att10 = Target(name='The Great Wall', destination_id=1, image='static/upload/great_wall.jpg', intro='The Great Wall is an ancient Chinese military fortification, a long, tall, strong and continuous wall.', type='0', price=40)
    att11 = Target(name='National Museum of China', destination_id=1, image='static/upload/museum.jpg', intro='National Museum of China is the highest historical and cultural art hall and cultural living room of the country.', type='0', price=120)
    att12 = Target(name='Temple of Heaven', destination_id=1, image='static/upload/temple.jpg', intro='The Temple of Heaven is the largest surviving ancient sacrificial complex in China.', type='0', price=30)


    # Shanghai
    att13 = Target(name='Shanghai Disney Resort', destination_id=2, image='static/upload/Disney.jpg', intro='Shanghai Disneyland not only retains the classic fairy tale style, but also incorporates more Chinese elements.', type='0', price=399)
    att14 = Target(name='Oriental Pearl Tower', destination_id=2, image='static/upload/tower.jpg', intro="The Oriental Pearl, adjacent to the Huangpu River and across the river from the Bund, is one of Shanghai's iconic cultural landscapes.", type='0', price=368)
    att15 = Target(name='The Bund', destination_id=2, image='static/upload/bund.jpg', intro='The Bund is the starting point of the modern city of Shanghai, and contains the essence of the whole city.', type='0', price=10)

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
                        tra2, tra3, tra4, tra5, att9, att10, att11, att12, att13, att14, att15, acc8, acc9, acc10])
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
    day11 = Day(id=11, destination_id=4, attraction_id=15, accommodation_id=6, traffic_id=17)

    # ---------------------------com4/5--------------------------------#
    day12 = Day(destination_id=1, attraction_id=21, accommodation_id=28, traffic_id=18)
    day13 = Day(destination_id=1, attraction_id=22, accommodation_id=28, traffic_id=18)
    day14 = Day(destination_id=1, attraction_id=23, accommodation_id=29, traffic_id=16)
    day15 = Day(destination_id=1, attraction_id=24, accommodation_id=29, traffic_id=17)

    # ---------------------------com6--------------------------------#
    day16 = Day(destination_id=2, attraction_id=25, accommodation_id=30, traffic_id=17)
    day17 = Day(destination_id=2, attraction_id=26, accommodation_id=30, traffic_id=20)
    day18 = Day(destination_id=2, attraction_id=27, accommodation_id=30, traffic_id=20)

    db.session.add_all([day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, day14, day15, day16, day17, day18])
    db.session.commit()

    com1 = Combination(name="New York Two-Day Trip", day1=1, day2=3, day3=None, day4=None, day5=None, day6=None, day7=None,
                       intro="Attractions includes the 9/11 Memorial and Museum and the Statue of Liberty. These iconic landmarks represent the city's rich history and culture.", price=3350, length=2, image='static/upload/Liberty.png')
    com2 = Combination(name='New York Four-Day Trip', day1=4, day2=5, day3=6, day4=7, day5=None, day6=None, day7=None,
                       intro="During this four-day tour, you'll visit iconic landmarks like the 9/11 Memorial and Museum and the Statue of Liberty, as well as attend a Broadway show and climb a skyscraper. Experience the unique charm of New York City on this unforgettable tour.", price=5250, length=4, image='static/upload/summit2.png')
    com3 = Combination(name='Dublin Four-Day Trip', day1=8, day2=9, day3=10, day4=11, day5=None, day6=None, day7=None,
                          intro='Explore the stunning Cliffs of Moher and vibrant Galway. Tour the iconic Jameson Distillery, hop on a convenient Hop-On Hop-Off tour, and kiss the Blarney Stone at the legendary Blarney Castle. An unforgettable adventure awaits!', price=4250, length=4, image='static/upload/Galway.png')
    com4 = Combination(name="Beijing Two-Day Trip", day1=13, day2=14, day3=None, day4=None, day5=None, day6=None,
                       day7=None,
                       intro="Attractions include the Great Wall and the National Museum of China, which gives visitors a glimpse of Beijing's cultural heritage, from military defenses to displays of treasures.",
                       price=2000, length=2, image='static/upload/great_wall.jpg')
    com5 = Combination(name='Beijing Four-Day Trip', day1=12, day2=13, day3=14, day4=15, day5=None, day6=None, day7=None,
                       intro='Beijing is a charming city with both classical charm and fashionable atmosphere. Explore the fascinating city of Beijing, on this tour we will visit the Forbidden City, the National Museum, the Great Wall and the Temple of Heaven.',
                       price=4300, length=4, image='static/upload/forbidden.jpg')
    com6 = Combination(name='Shanghai Three-Day Trip', day1=16, day2=17, day3=18, day4=None, day5=None, day6=None, day7=None,
                       intro='Shanghai, a commercial center where wealth converges, a magical metropolis with the name of "Paris of the East". During this trip, we will visit the interesting Disneyland, the landmark Oriental Pearl, and the bustling Bund.',
                       price=3100, length=3, image='static/upload/Disney.jpg')

    db.session.add_all([com1, com2, com3, com4, com5, com6])
    db.session.commit()

    fav1 = Favorite(user_id=3, target_id=1, time="2023-04-13 11:07:43")
    fav2 = Favorite(user_id=3, target_id=5, time="2023-02-13 10:00:33")
    fav3 = Favorite(user_id=3, target_id=10, time="2023-02-13 10:00:33")
    fav4 = Favorite(user_id=3, target_id=13, time="2023-02-13 10:00:33")
    fav5 = Favorite(user_id=3, target_id=14, time="2023-02-13 10:00:33")
    fav6 = Favorite(user_id=3, target_id=8, time="2023-02-13 10:00:33")
    fav9 = Favorite(user_id=3, target_id=19, time="2023-02-13 10:00:33")
    fav7 = FavoriteC(user_id=3, combination_id=1, time="2023-02-13 10:00:33")
    fav8 = FavoriteC(user_id=3, combination_id=2, time="2023-02-13 10:00:33")
    fav17 = Favorite(user_id=4, target_id=8, time="2023-02-13 10:00:33")
    fav10 = Favorite(user_id=4, target_id=11, time="2023-02-13 10:00:33")
    fav11 = Favorite(user_id=4, target_id=14, time="2023-02-13 10:00:33")
    fav12 = Favorite(user_id=4, target_id=29, time="2023-02-13 10:00:33")
    fav13 = Favorite(user_id=5, target_id=12, time="2023-02-13 10:00:33")
    fav14 = Favorite(user_id=5, target_id=26, time="2023-02-13 10:00:33")
    fav15 = Favorite(user_id=5, target_id=26, time="2023-02-13 10:00:33")
    fav16 = Favorite(user_id=6, target_id=15, time="2023-02-13 10:00:33")


    db.session.add_all([fav1, fav2, fav3, fav4, fav5, fav6, fav7, fav8, fav9, fav10, fav11, fav12, fav13, fav14, fav15, fav16, fav17])
    db.session.commit()


    # ---------------------------comment--------------------------------#
    comment1 = CommentC(user_id=4, username="allen", score=4, combination_id=3, content="This is a good trip! I was with my parents and they all said they feel very satisfied.", image="static/upload/Blarney.png", time="2023-02-13 10:00:33")
    comment2 = CommentC(user_id=5, username="chiquita", score=5, combination_id=3, content="Excellent trip! I even want to travel it again!", image="static/upload/Blarney.png", time="2023-04-13 11:05:33")
    comment3 = CommentC(user_id=6, username="Lily", score=5, combination_id=2,
                        content="Nice Trip! New York is so attractive! I will come again!", image="static/upload/New.png", time="2023-05-01 15:02:03")
    comment4 = CommentC(user_id=5, username="chiquita", score=5, combination_id=2,
                        content="The hotel can be better, else is nice", image="",
                        time="2023-05-03 13:19:30")
    comment5 = CommentC(user_id=6, username="Lily", score=5, combination_id=1,
                        content="Excellent trip! Nice hotel!", image="static/upload/New.png",
                        time="2023-04-13 11:05:33")
    comment6 = CommentC(user_id=7, username="jenny", score=4, combination_id=1,
                        content="Not perfect, but worthy to come!", image="static/upload/New.png",
                        time="2023-04-23 11:15:33")
    comment7 = CommentC(user_id=4, username="allen", score=4, combination_id=5,
                        content="This is a good trip! I was with my parents and they all said they feel very satisfied.",
                        image="static/upload/comment_bj.jpg", time="2023-02-13 10:00:33")
    comment8 = CommentC(user_id=5, username="chiquita", score=5, combination_id=5,
                        content="Excellent trip! I even want to travel it again!", image="static/upload/comment_bj2.jpg",
                        time="2023-04-13 11:05:33")
    comment9 = CommentC(user_id=6, username="Lily", score=5, combination_id=5,
                        content="Nice Trip! Beijing is so attractive! I will come again!",
                         time="2023-05-01 15:02:03")
    comment10 = CommentC(user_id=5, username="chiquita", score=4, combination_id=6,
                        content="The hotel can be better, else is nice", image="",
                        time="2023-05-03 13:19:30")
    comment11 = CommentC(user_id=6, username="Lily", score=5, combination_id=6,
                        content="Excellent trip! Nice hotel!", image="static/upload/New.png",
                        time="2023-04-13 11:05:33")
    comment12 = CommentC(user_id=7, username="jenny", score=4, combination_id=6,
                        content="Not perfect, but worthy to come!", image="static/upload/New.png",
                        time="2023-04-23 11:15:33")
    comment13 = Comment(user_id=4, username="allen", score=4, target_id=1, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment14 = Comment(user_id=4, username="allen", score=4, target_id=2, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment15 = Comment(user_id=4, username="allen", score=4, target_id=3, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment16 = Comment(user_id=4, username="allen", score=4, target_id=8, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment17 = Comment(user_id=4, username="allen", score=4, target_id=9, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment18 = Comment(user_id=4, username="allen", score=4, target_id=10, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment19 = Comment(user_id=4, username="allen", score=4, target_id=11, content="It's worth a visit", time="2023-04-23 11:15:33")
    comment20 = Comment(user_id=5, username="chiquita", score=5, target_id=1, content='It was very nice and touched me deeply, I hope to have the opportunity to visit again', time="2023-05-01 15:02:03")
    comment21 = Comment(user_id=5, username="chiquita", score=5, target_id=2, content='It was very nice and touched me deeply, I hope to have the opportunity to visit again', time="2023-05-01 15:02:03")
    comment22 = Comment(user_id=5, username="chiquita", score=4, target_id=12, content='It was very nice and touched me deeply, I hope to have the opportunity to visit again', time="2023-05-01 15:02:03")
    comment23 = Comment(user_id=5, username="chiquita", score=5, target_id=13, content='It was very nice and touched me deeply, I hope to have the opportunity to visit again', time="2023-05-01 15:02:03")
    comment24 = Comment(user_id=5, username="chiquita", score=4, target_id=14, content='It was very nice and touched me deeply, I hope to have the opportunity to visit again', time="2023-05-01 15:02:03")
    comment25 = Comment(user_id=5, username="chiquita", score=5, target_id=8, content='It was very nice and touched me deeply, I hope to have the opportunity to visit again', time="2023-05-01 15:02:03")
    comment26 = Comment(user_id=6, username="Lily", score=5, target_id=21, content='nice, I was blown away by the beauty of the scenery', time="2023-05-07 17:17:03")
    comment27 = Comment(user_id=6, username="Lily", score=5, target_id=22, content='nice, I was blown away by the beauty of the scenery', time="2023-05-07 17:17:03")
    comment28 = Comment(user_id=6, username="Lily", score=5, target_id=23, content='nice, I was blown away by the beauty of the scenery', time="2023-05-07 17:17:03")
    comment29 = Comment(user_id=6, username="Lily", score=5, target_id=8, content='nice, I was blown away by the beauty of the scenery', time="2023-05-07 17:17:03")
    comment30 = Comment(user_id=6, username="Lily", score=5, target_id=12, content='nice, I was blown away by the beauty of the scenery', time="2023-05-07 17:17:03")

    db.session.add_all([comment1, comment2,comment3,comment4,comment5,comment6, comment7, comment8, comment9, comment10, comment11, comment12, comment13,comment14,comment15,comment16,comment17,comment18,comment19,comment20,comment21,comment22,comment23,comment24,comment25,comment26,comment27,comment28,comment29,comment30])
    db.session.commit()


    # ---------------------------order--------------------------------#
    order1 = RecordC(user_id=3, combination_id=1, time="2023-02-13 10:00:33", start_time="2023-07-13", num=2, name="Selina", tel=11010801234, price=3350, status="Uncompleted", status2="No comment")
    order2 = RecordC(user_id=6, combination_id=1, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="Lily", tel=18932523251, price=3250, status="Completed", status2="Commented")
    order3 = RecordC(user_id=7, combination_id=1, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="jenny", tel=18932523251, price=3250, status="Completed", status2="Commented")

    order4 = RecordC(user_id=5, combination_id=2, time="2023-03-19 05:18:58", start_time="2023-05-20", num=2, name="chiquita", tel=18910191225, price=5250, status="Completed", status2="Commented")
    order5 = RecordC(user_id=6, combination_id=2, time="2023-03-19 05:18:58", start_time="2023-05-20", num=2,
                     name="Lily", tel=18910191225, price=5250, status="Completed", status2="Commented")

    order6 = RecordC(user_id=5, combination_id=3, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="chiquita", tel=18932523251, price=3250, status="Completed", status2="Commented")
    order7 = RecordC(user_id=4, combination_id=3, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="allen", tel=18932523251, price=3250, status="Completed", status2="Commented")

    order8 = RecordC(user_id=3, combination_id=5, time="2023-02-15 17:17:33", start_time="2023-04-13", num=2, name="Selina", tel=11010801234, price=3350, status="Completed", status2="No comment")
    order9 = RecordC(user_id=6, combination_id=5, time="2023-03-19 05:18:58", start_time="2023-05-20", num=2,
                     name="Lily", tel=18910191225, price=5250, status="Completed", status2="Commented")

    order10 = RecordC(user_id=5, combination_id=5, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="chiquita", tel=18932523251, price=3250, status="Completed", status2="Commented")
    order11 = RecordC(user_id=4, combination_id=5, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="allen", tel=18932523251, price=3250, status="Uncompleted", status2="No comment")

    order12 = RecordC(user_id=7, combination_id=6, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                     name="jenny", tel=18932523251, price=3250, status="Uncompleted", status2="No comment")
    order13 = RecordC(user_id=6, combination_id=6, time="2023-03-19 05:18:58", start_time="2023-05-20", num=2,
                     name="Lily", tel=18910191225, price=5250, status="Completed", status2="Commented")

    order14 = RecordC(user_id=5, combination_id=6, time="2023-03-09 05:18:58", start_time="2023-05-12", num=2,
                      name="chiquita", tel=18932523251, price=3250, status="Completed", status2="Commented")

    db.session.add_all([order1, order2,order3,order4,order5,order6,order7,order8,order9,order10,order11,order12,order13,order14])
    db.session.commit()


    # ---------------------------customised package--------------------------------#
    package1 = UserCombination(3,'selina','Take a tour around the Bund and see the Oriental Pearl',400,2,17,18,None,None,None,None,None)
    package2 = UserCombination(3,'selina','A short trip in beautiful Dublin',570,2,9,10,None,None,None,None,None)

    db.session.add_all([package1,package2])
    db.session.commit()

    # ---------------------------contact us-------------------------------#
    contact1 = ContactModel(email='1587986524@163.com',name='Yudu',message='Thank you for your website! Very convenient operation that has made for many perfect trips for my family, which has made our family bond even better! I will continue to support you in the future, thanks again!')
    contact2 = ContactModel(email='Runningwheel@rnw.com', name='Hans', message='Hello, I am a member of the Drive Wheel staff and would like to ask if we have the opportunity to discuss the possibility of business cooperation with your company. Looking forward to hearing from you.')
    contact3 = ContactModel(email='Lily@ucd.ie', name='Lily', message='Your site made it easy for me to book a trip, but I wish you had a more aesthetically pleasing home page, it might help your site attract more users.')
    db.session.add_all([contact1, contact2,contact3])
    db.session.commit()