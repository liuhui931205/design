from flask import Blueprint

member = Blueprint('member', __name__)

from .views import *