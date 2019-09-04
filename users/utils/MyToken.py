# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 19:10
# @Author  : tuihou
# @File    : MyToken.py

# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 23:01
# @Author  : tuihou
# @File    : token.py
from MyApi.settings import SECRET_KEY


def get_random_token(username):
    """
    根据用户名和时间戳生成随机token
    :param username:
    :return:
    """
    import hashlib, time
    timestamp = str(time.time()) + SECRET_KEY
    m = hashlib.md5(bytes(username, encoding="utf8"))
    m.update(bytes(timestamp, encoding="utf8"))
    return m.hexdigest()
