# Flask configuration files
# https://flask.readthedocs.org/en/0.6.1/config/


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECRET_KEY = '\x1d#\xa4\xa3\xde\xa2\xb4\xf73\x0e\x96ybO!\x1a\xf8\xbf\xcc\t\xdd\xc1WH'
    FILE_PER_PAGE = 10


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestinConfig(Config):
    BABEL_DEFAULT_LOCALE = 'en_US'
    TESTING = True
