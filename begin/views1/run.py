# -*- coding: utf-8 -*-
# @Time    : 2019/6/2 10:54
# @Author  : tuihou
# @File    : run.py
import json
from begin.utils.parse import debug_case
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.utils.response import JsonResponse
from rest_framework.views import APIView
from begin.utils.prepare import build_case
from rest_framework import status


class RunCaseByBodyView(APIView):

    def post(self, request):
        try:
            data = json.loads(json.dumps(request.data))
            config = data['config']
            steps = data['steps']
            case_name = data['caseName']
            case_steps = build_case(steps, case_name=case_name)
            summary = debug_case(case_steps, config=config)
            return JsonResponse(data=summary, code=2001, status=status.HTTP_200_OK, msg='success')
        except ValueError:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, code=4001, msg='not found')