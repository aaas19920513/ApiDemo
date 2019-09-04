# -*- coding: utf-8 -*-
# @Time    : 2019/8/18 12:54
# @Author  : tuihou
# @File    : tools.py

import re
from faker import Faker
import functools
from threading import Thread
sign_regex_compile = re.compile(r"\@\@")


def get_func(content):
    """
    判断是否@开头，再判断是否是@@开头
    :param content:
    :return:
    """
    try:
        match_start_position = content.index("@", 0)

    except ValueError:
        return content

    match_sign = sign_regex_compile.match(content, match_start_position)
    if match_sign:
        match_start_position = match_sign.end()
    else:
        match_start_position += 1

    func_name = content[match_start_position:]

    if len(func_name) == 0:
        return content

    return func_name


def is_faker_func(content):
    func_name = get_func(content)
    try:
        obj = getattr(Faker(locale='zh_CN'), func_name)
    except:
        return content
    return obj()


def run_fast(func):

    # http: // www.hongweipeng.com / index.php / archives / 1814 /
    # 保持当前装饰器装饰函数的 __name__ 的值不变

    @functools.wraps(func)
    def inner(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return inner