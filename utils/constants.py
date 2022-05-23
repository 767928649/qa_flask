# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 下午2:24
# @Author  : Ly
"""
常量配置
"""
from enum import Enum


class UserStatus(Enum):
    """用户状态"""
    # 启用,可以登录系统
    user_active = 1
    # 禁用.不能登录系统
    user_in_active = 0


class UserRole(Enum):
    """
    用户角色
    """
    # 普通用户
    common = 0
    # 管理员库使用后台功能
    admin = 1
    # 超级管理员
    super_admin = 2
