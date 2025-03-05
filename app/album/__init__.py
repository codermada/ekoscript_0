from flask import Blueprint

album = Blueprint('album', __name__)

from . import views