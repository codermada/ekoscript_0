from flask import Blueprint

supgroup = Blueprint('supgroup', __name__)

from . import views