from flask import Blueprint

illustration = Blueprint('illustration', __name__)

from . import views