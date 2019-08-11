# -*- coding: utf-8 -*-
# @Time    : 2019/6/2 10:54
# @Author  : tuihou
# @File    : run.py
import json
from begin.utils.debug import Format2, debug_case
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def run_api(request):
    """ run api by body
    """
    data = request.body
    req_data = json.loads(data)
    api = Format2(req_data, level='test')
    api.parse()
    summary = debug_case(api.testcase)
    return Response(summary)