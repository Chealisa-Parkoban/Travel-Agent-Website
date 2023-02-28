
class Config(object):

    user = 'root'
    password = 'cyw081902'
    host = 'localhost'
    port = '3306'
    database = 'travelAgent'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + user + ':' + password + '@localhost:' + port + '/' + database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_BINDS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
