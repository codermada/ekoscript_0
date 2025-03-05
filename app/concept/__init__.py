from flask import Blueprint

concept = Blueprint('concept', __name__)

from . import views