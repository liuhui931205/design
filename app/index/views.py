import time
from app.index import index
from flask import request, jsonify, g
from app.models import *
from app import db
from util import qiniu_auth


@index.route('/get_token')
def get_up_token():
    token = qiniu_auth.get_qiu_auth().upload_token("liuhui-12")
    key = str(int(time.time()))
    resp = jsonify(code=0, data={"token": token, "key": key}, message="查询成功")
    return resp


@index.route('/get_bannars')
def get_bannars():
    li = qiniu_auth.get_bucket(prefix="banner")
    resp = jsonify(code=0, data=li, message="查询成功")
    return resp

@index.route('/get_recommend')
def get_recommend():
    results = db.session.query(ShuYanRecommend).order_by(ShuYanRecommend.sort_num).all()
    data = []
    for o in results:
        data.append({
            "imgUrl": o.img_url, "name": o.name, "id": o.ref_code
        })
    resp = jsonify(code=0, data=data, message="查询成功")
    return resp

@index.route('/get_feature')
def get_feature():
    results = db.session.query(ShuYanCommodity).all()[:4]
    data = []
    for o in results:
        data.append(o.to_dict())
    resp = jsonify(code=0, data=data, message="查询成功")
    return resp


