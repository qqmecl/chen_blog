import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10
    FLASKY_MAIL_SUBJECT_PREFIX = 'chen_blog'
    FLASKY_MAIL_SENDER = 'chen<qq562554268@163.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
        DEBUG = True
        MAIL_SERVER = 'smtp.163.com'
        MAIL_PORT = 465
        MAIL_USE_SSL = True
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                  'sqlite:///' + os.path.join(basedir, 'data_dev.sqlite')

class TestingConfig(Config):
        TESTING = True
        WTF_CSRF_ENABLED = False
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                  'sqlite:///' + os.path.join(basedir, 'data_test.sqlite')

class ProductionConfig(Config):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                  'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,

    'default' : DevelopmentConfig
}
