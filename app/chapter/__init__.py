from flask import Blueprint

chapter = Blueprint('chapter', __name__)

from . import views