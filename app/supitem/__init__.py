from flask import Blueprint

supitem = Blueprint('supitem', __name__)

from . import views