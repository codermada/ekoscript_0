from flask import Blueprint

supcharacter = Blueprint('supcharacter', __name__)

from . import views