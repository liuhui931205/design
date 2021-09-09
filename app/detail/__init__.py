from flask import Blueprint

detail = Blueprint('detail', __name__)

from .views import *
