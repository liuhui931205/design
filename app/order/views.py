from app.order import order
from flask import request, jsonify, g
from app.models import *
from app import db


@order.route('/getPhone', methods=["POST"])
def bing_customer():
    pass