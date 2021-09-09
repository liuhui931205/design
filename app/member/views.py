from app.member import member
from flask import request, jsonify, g
from app.models import *
from app import db, redis_store
from util import utils
from util.utils import get_short_uuid


@member.route('/get_phone', methods=["POST"])
def get_phone():
    req_dict = request.json
    encryptedData = req_dict.get('encrypdata')
    vinum = req_dict.get('ivdata')
    openid = req_dict.get('openid')

    # 处理加密的手机号
    # encryptedData = encryptedData + '=='

    # 获取加密向量

    # 处理加密向量
    # iv = vinum + '=='

    # 获取openid

    # appid
    APPID = "wxc7e5c2fc9da0296a"
    appId = APPID

    # 获取sessinkey
    # redis_conn = get_redis_connection('session_key')
    # sessionKey = redis_conn.get('session_key_%s' % openid)
    sessionKey = req_dict.get('sessionkey')

    # 解密手机号
    pc = utils.WXBizDataCrypt(appId, sessionKey)
    mobile_obj = pc.decrypt(encryptedData, vinum)
    mobile = mobile_obj['phoneNumber']
    print(mobile)
    data = {'mobile': mobile}
    resp = jsonify(code=0, data=data, message="查询成功")
    return resp


@member.route('/login', methods=["POST"])
def login():
    req_dict = request.json
    phone = req_dict.get('phone')
    code = req_dict.get('code')

    # e_code = redis_store.hget("code",phone)
    if code == "111111":
        resp = jsonify(code=0, data="", message="success")
    else:
        resp = jsonify(code=-1, data="", message="error")
    return resp


@member.route('/get_code', methods=["POST"])
def get_code():
    req_dict = request.json
    phone = req_dict.get('phone')

    # redis_store.hset("code",phone,"111111")
    resp = jsonify(code=0, data="", message="查询成功")
    return resp


@member.route('/register', methods=["POST"])
def register():
    req_dict = request.json
    phone = req_dict.get('phone')
    name = req_dict.get('nickName', f"用户_{get_short_uuid()}")
    url = req_dict.get('avatarUrl', "http://qwuj9bu2d.hb-bkt.clouddn.com/avatar.png")
    gender = req_dict.get('gender')
    if db.session.query(ShuYanUser.id).filter(ShuYanUser.phone == phone).scalar():
        o = db.session.query(ShuYanUser).filter(ShuYanUser.phone == phone).first()

        data = o.to_dict()
        resp = jsonify(code=0, data=data, message="查询成功")
    else:
        user = ShuYanUser()
        user.phone = phone
        user.name = name
        user.url = url
        user.gender = gender
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    # redis_store.hset("code",phone,"111111")
        resp = jsonify(code=0, data={"phone":phone,"name":name,"url":url,"gender":gender}, message="查询成功")
    return resp
