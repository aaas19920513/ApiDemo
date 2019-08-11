# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 22:01
# @Author  : tuihou
# @File    : prepare.py

from begin import models
import requests

def build_case(pk):
    """build case by pk"""
    step_data = models.Case.objects.filter(pk=pk).first
    if not step_data:
        return ('error')
    if not step_data['step']:
        return('no step')
    print(step_data)
    return step_data


def run_api(api_dict):
    print('ssssssssssssssssssssssss')
    body = {}
    api_data = api_dict
    if not api_data:
        return ('error')
    url = api_data['url']
    method = api_data['method']
    if api_data['body']:
        body = api_data['body']
    if not url or not method:
        return ('error')
    print('111111111111111111')
    a = requests.request(url=url, method=method, )
    print('222222222222222222222222')
    return a


