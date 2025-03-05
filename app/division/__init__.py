from flask import Blueprint

division = Blueprint('division', __name__)

from . import views