import time
from app.detail import detail
from flask import request, jsonify, g
from app.models import *
from app import db
from util import qiniu_auth


@detail.route('/get_list')
def get_list():
    query_type = request.args.get('type')
    page = request.args.get('page')
    results = db.session.query(ShuYanCommodity).paginate(page=int(page),per_page=10, error_out=False)
    data = []
    for o in results.items:
        data.append(o.to_dict())
    resp = jsonify(code=0, data=data, message="查询成功")
    return resp


@detail.route('/get_detail')
def get_detail():
    query_id = request.args.get('id')
    results = db.session.query(ShuYanCommodityDetail).filter(
        ShuYanCommodityDetail.commodity_id == int(query_id)).first()
    d = results.to_dict()
    resp = jsonify(code=0, data=d, message="查询成功")
    return resp

@detail.route('/get_style')
def get_style():
    query_id = request.args.get('id')
    sku = db.session.query(ShuYanCommodityStyle).filter(ShuYanCommodityStyle.commodity_id == int(query_id)).all()
    data = [o.to_dict() for o in sku]
    result = {}
    color = list(set([o["color"] for o in data]))
    color_map = {}
    for o in data:
        if o["color"] not in color_map:
            color_map[o["color"]] = []
        color_map[o["color"]].append({"text":o["properties"],"disable":True if o["inventory"] >0 else False})
    for k,v in color_map.items():
        for i in range(len(v)):
            v[i]["value"] = i

    result["color"] = [{"value":i,"text":color[i] } for i in range(len(color))]
    result["maps"] = color_map

    resp = jsonify(code=0, data=result, message="查询成功")
    return resp
