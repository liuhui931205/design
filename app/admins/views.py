import time

from sqlalchemy import func

from app.admins import admin
from flask import request, jsonify, g
from app.models import *
from app import db
from util.qiniu_auth import upload_data,BASE_URL


@admin.route('/up_recommend',methods=["POST"])
def up_recommend():
    # results = db.session.query(ShuYanRecommend).all()
    # for i in results:
    #     print(i)
    ti = int(time.time())
    img = request.files.get("image")
    ind = request.form.get("ind")

    maps = {
        "cost":"高性价比",
        "new":"新品上新",
        "qual":"品质甄选",
        "manu":"大牌制造",
    }
    upload_data(f"{ti}",img)
    img_url = f"{BASE_URL}{ti}"
    obj = db.session.query(ShuYanRecommend).filter(ShuYanRecommend.ref_code == ind).first()
    if obj:
        obj.img_url = img_url
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        # db.session.query(ShuYanRecommend).filter(ShuYanRecommend.ref_code == ind).first()
        s = db.session.query(func.max(ShuYanRecommend.sort_num).label("max_num")).one()
        if s[0]:
            recommend = ShuYanRecommend(ref_code=ind,img_url=img_url,sort_num=s[0]+1,name=maps[ind])
        else:
            recommend = ShuYanRecommend(ref_code=ind, img_url=img_url, sort_num=1, name=maps[ind])
        db.session.add(recommend)
        db.session.commit()
    # li = qiniu_auth.get_bucket(prefix="recommend")
    # l = ["高性价比","新品上新","品质甄选","大牌制造"]
    # data = []
    # for i in range(len(li)):
    #     data.append({"imgUrl":li[i],"name":l[i],"id":i+1})

    resp = jsonify(code=0, data="", message="查询成功")
    return resp