class BaseConfig(object):
    SECRET_KEY = 'this is flask-blog.'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xqxq1994@localhost:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BLOG_PER_PAGE = 10
    ADMIN_PER_PAGE = 15

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    Testing = True

configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

