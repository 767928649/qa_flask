# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 下午3:45
# @Author  : Ly
import os


class Config(object):
    """项目配置文件"""
    # 数据库连接
    user = 'root'
    password = 'root'
    database = 'flask_qa'
    uri = 'mysql+pymysql://%s:%s@101.33.231.53:3306/%s' % (user, password, database)
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, 秘钥
    SECRET_KEY = os.urandom(24)
    # 文件上传路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "medias")
