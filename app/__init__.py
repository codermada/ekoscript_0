from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager 

from config import config


db = SQLAlchemy()
bootstrap = Bootstrap5()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

photos = UploadSet('photos', IMAGES)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    configure_uploads(app, photos)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')

    from .concept import concept as concept_blueprint
    app.register_blueprint(concept_blueprint, url_prefix='/concept')

    from .supcharacter import supcharacter as supcharacter_blueprint
    app.register_blueprint(supcharacter_blueprint, url_prefix='/supcharacter')

    from .character import character as character_blueprint
    app.register_blueprint(character_blueprint, url_prefix='/character')

    from .illustration import illustration as illustration_blueprint
    app.register_blueprint(illustration_blueprint, url_prefix='/illustration')

    from .supgroup import supgroup as supgroup_blueprint
    app.register_blueprint(supgroup_blueprint, url_prefix='/supgroup')

    from .group import group as group_blueprint
    app.register_blueprint(group_blueprint, url_prefix='/group')

    from .supitem import supitem as supitem_blueprint
    app.register_blueprint(supitem_blueprint, url_prefix='/supitem')

    from .item import item as item_blueprint
    app.register_blueprint(item_blueprint, url_prefix='/item')

    from .chapter import chapter as chapter_blueprint
    app.register_blueprint(chapter_blueprint, url_prefix='/chapter')

    from .panel import panel as panel_blueprint
    app.register_blueprint(panel_blueprint, url_prefix='/panel')

    from .division import division as division_blueprint
    app.register_blueprint(division_blueprint, url_prefix='/division')

    from .album import album as album_blueprint
    app.register_blueprint(album_blueprint,  url_prefix='/album')

    from .photo import photo as photo_blueprint
    app.register_blueprint(photo_blueprint, url_prefix='/photo')

    return app
