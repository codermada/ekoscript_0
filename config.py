import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'random secret key 123456789azertyuiop'
    PER_PAGE = 20
    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-data.db')
    BOOTSTRAP_SERVE_LOCAL = True
    UPLOADED_PHOTOS_DEST = basedir+"/app/static/tmp"


config = {
    'default': DevConfig
}