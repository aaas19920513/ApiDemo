# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 17:56
# @Author  : tuihou
# @File    : response_dict.py


miss_value_dict = {
    'code': 2001,
    'msg': '请求数据非法',
}

success_dict = {
    'code': 2001,
    'msg': 'success',
}

token_dict = {
    'code': 2001,
    'msg': 'success',
    'token': None,
    'username': None,
}

login_failed = {
    'code': 2002,
    'msg': '用户名或密码错误,请重试',
}

register_failed = {
    'code': 2001,
    'msg': '注册失败，用户名已存在',
}

auth_failed = {
    'code': '2005',
    'msg': '用户认证失败',
}