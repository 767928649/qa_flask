# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 下午7:51
# @Author  : Ly


def number_split(num):
    """
    数字格式化
    123456 > 12,345, 678
    :param num: 需要格式化的数字
    :return: 格式化后的字符串
    """
    # return '%s,' % int(num)
    return '{:3,}'.format(int(num))
