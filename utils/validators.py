# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 下午1:34
# @Author  : Ly
import re
from datetime import datetime

import timeago
from wtforms.validators import ValidationError


def phone_number(form, username):
    """手机号码验证"""
    username = username.data
    pattern = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    if not re.search(pattern, username):
        raise ValidationError('请输入正确的手机号')
    return username


def dt_format_show(dt):
    """
    日期和时间格式化显示
    :param dt: 时间
    :return: 返回格式化的时间
    """
    now = datetime.now()
    return timeago.format(dt, now, 'zh_CN')