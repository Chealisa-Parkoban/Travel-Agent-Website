from travelAgent.models import User
from travelAgent import db
from travelAgent import app

with app.app_context():
    db.drop_all() # 删除存在表
    db.create_all() # 创建这两个表

    us1 = User(username='wang', email='wang@163.com')
    db.session.add_all([us1])
    db.session.commit()