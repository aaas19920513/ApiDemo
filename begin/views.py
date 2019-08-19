from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins, generics
from .serializers import ProjectSerializer, CaseSerializer, StepSerializer, VariablesSerializer, ApiSerializer, ClassifySerializer
from begin import models
from rest_framework.response import Response
from django.core import exceptions
import json
import requests
from begin.utils.prepare import build_case, build_case_by_id
from begin.utils.parse import debug_cases, ParseStepFromClient, debug_case
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from rest_framework import status
from users.utils.response import JsonResponse

not_exict = {
    'code': '2004',
    'msg': 'sorry this obj is not exict '
}


class RunSingleApi(GenericViewSet):
    queryset = models.API.objects.all().order_by()
    serializer_class = ApiSerializer
    authentication_classes = []

    def single(self, request,  **kwargs):
        pk = kwargs.pop('pk')
        try:
            queryset = models.API.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist:
            return Response(not_exict)
        serializer = self.get_serializer(queryset, many=False)
        data = json.dumps(serializer.data)
        eval(data)
        print(type(data))
        url = data['url']
        method = data['method']
        if not url or not method:
            return Response('Error')
        resp = requests.request(url=url, method=method)
        return Response(resp)


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

# @api_view(['POST'])
# def run_case(request):
#     """
#     run case by request data
#     :param request:{
#       'config': {},
#       'casename': '',
#       'steps': [],
# }
#     :return:
#     """
#     data = request.body
#     req_data = json.loads(data)
#     steps = req_data['steps']
#     casename = req_data['casename']
#     config = req_data['config']
#     case_steps = build_case(steps)
#     summary = debug_case(case=case_steps, casename=casename, config=config)
#
#     return Response(summary)


# @api_view(['POST'])
# def run_case_by_id(request):
#     """
#
#     :param request: {id:[]}
#     :return:
#     """
#     data = request.body
#     req_data = json.loads(data)
#     id = req_data['id']
#     casename = req_data['casename']
#     config = req_data['config']
#     case_steps = build_case(steps)
#     summary = debug_case(case=case_steps, casename=casename, config=config)
#
#     return Response(summary)


@api_view(['POST'])
def run_case_by_id(request):
    """
    :param request:  {'case_id': [1,2,3]}
    :return:
    """
    try:
        data = request.body
        req_data = json.loads(data)
        list_id = req_data['case_id']
        config = req_data['config']
        # config = req_data['config']
        # if list_id is None:
        #     return Response('fail， 参数有误')
        cases = build_case_by_id(list_id)
        debug_cases(cases=cases, config=config)
        return Response('test')
    except:
        return Response('fail')
