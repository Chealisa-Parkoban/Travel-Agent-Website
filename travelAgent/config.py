
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

    # user = 'debian-sys-maint'
    # password = 'tBhcNDnb3ieforAr'
    # host = 'localhost'
    # port = '3306'
    # database = 'travelAgent'
    #
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + user + ':' + password + '@localhost:' + port + '/' + database
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # # SQLALCHEMY_BINDS = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮箱配置
    # 用自己邮箱qq邮箱
    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    # MAIL_USERNAME = "3089691062@qq.com"
    MAIL_USERNAME = "15210087572@163.com"
    # MAIL_PASSWORD = "gmcpykwckboaddje"
    # MAIL_PASSWORD = 'ohumgeihybrgddfi'
    MAIL_PASSWORD = 'PLZEDVYDFBXRXJJX'
    # MAIL_DEFAULT_SENDER = "3089691062@qq.com"
    MAIL_DEFAULT_SENDER = "15210087572@163.com"
