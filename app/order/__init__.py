from flask import Blueprint

order = Blueprint('order', __name__)

from .views import *