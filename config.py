# -*- coding: UTF-8 -*-
import os
import urllib.parse
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_DIR = os.path.join(basedir, 'logs')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACH_MODIFICATIONS = True


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DATA_DIR = basedir

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost:3306/design?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,"design.sqlite")
    # SQLALCHEMY_BINDS = {
    #     'design': 'mysql+mysqlconnector://root:LiuHui931205@42cdc50388234f72bb93703e13d16270in01.internal.cn-north-4.mysql.rds.myhuaweicloud.com:3306/estateinfo?charset=utf8'
    # }
    # SQLALCHEMY_POOL_SIZE = 30
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIST_DB = 4




class ProductionConfig(Config):
    LOG_DIR = os.path.join(os.path.dirname(basedir), 'logs')
    DATA_DIR = os.path.join(os.path.dirname(basedir), 'data')
    CLICKHOUSE_ENV = "production"
    CLICKHOUSE_TABLE = "detailsinfo"
    # DEBUG = True
    # SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:LiuHui931205@42cdc50388234f72bb93703e13d16270in01.internal.cn-north-4.mysql.rds.myhuaweicloud.com:3306/design?charset=utf8'
    SQLALCHEMY_POOL_SIZE = 30
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIST_DB = 4


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
