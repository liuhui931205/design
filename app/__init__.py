from flask import Flask, jsonify,g, make_response
from flask_cors import CORS
import redis
from config import config
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
redis_store = None

def app_create(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # app = Flask('DataDelivery')
    app.config.from_object(config[config_name])
    # 设置是否跟踪数据库的修改情况，一般不跟踪
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 数据库操作时是否显示原始SQL语句，一般都是打开的，因为我们后台要日志
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 5
    config[config_name].init_app(app)
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT, db=config[config_name].REDIST_DB)
    # cors.init_app(app=app,resources={r"/*": {"origins": "*"}})


    from app.order import order
    from app.member import member
    from app.index import index
    from app.admins import admin
    from app.detail import detail

    # limiter = Limiter(app, default_limits=["5/second"], key_func=get_user_name)
    # limiter = Limiter(app, default_limits=["5/second"], key_func=get_remote_address)
    # limiter.limit("2/day")(customer_blueprint)
    # limiter.limit("2/day")(report_blueprint)
    # limiter.limit("2/day")(media_blueprint)

    # app.register_blueprint(auth_blueprint, url_prefix="/user/")
    # app.register_blueprint(organization_blueprint, url_prefix="/user/")

    app.register_blueprint(order, url_prefix="/order/")
    app.register_blueprint(member, url_prefix='/member/')
    app.register_blueprint(index, url_prefix='/index/')
    app.register_blueprint(admin, url_prefix='/admin/')
    app.register_blueprint(detail, url_prefix='/detail/')
    return app