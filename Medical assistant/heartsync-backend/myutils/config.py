import os


class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_DEFAULT_SENDER = 'heartsync2021@gmail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PASSWORD = 'HeartSync2021'
    MAIL_USERNAME = 'heartsync2021@gmail.com'
    SCAN_FILES = 'file/files'


class ProductionConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    FLASK_DEBUG = 1


class TestingConfig(Config):
    TESTING = True
