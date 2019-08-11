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
from django.forms.models import model_to_dict

not_exict = {
    'code': '2004',
    'msg': 'sorry this obj is not exict '
}


class RunSingleTestCase(GenericViewSet):

    queryset = models.Case.objects.all().order_by('update_time')
    serializer_class = CaseSerializer
    authentication_classes = []

    def single(self, request, **kwargs):
        pk = kwargs.pop('pk')

        try:
            queryset = models.Case.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist:
            return Response(not_exict)
        serializer = self.get_serializer(queryset, many=False)
        print(serializer.data)
        return Response(serializer.data)


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

# from begin.utils import prepare
# @api_view(['POST'])
# def run_api(request):
#     data = request.data
#     url = data['url']
#     method = data['method']
#     print(data)
#     print(url)
#
#     a = requests.request(url=url, method=method)
#     # a = 'sss'
#     print(a.text)
#     return Response(a.text)

from begin.utils.debug import Format2, debug_case, build_case, build_case_by_id, debug_cases
from django.core import serializers
from django.http import QueryDict

@api_view(['POST'])
def run_api(request):
    """ run single api by body
    """
    data = request.body
    req_data = json.loads(data)
    api = Format2(req_data, level='test')
    api.parse()
    summary = debug_case(api.testcase)
    return Response(summary)


@api_view(['POST'])
def run_case(request):
    """
    run case by request data
    :param request:{
      'config': {},
      'casename': '',
      'steps': [],
}
    :return:
    """
    data = request.body
    req_data = json.loads(data)
    steps = req_data['steps']
    casename = req_data['casename']
    config = req_data['config']
    case_steps = build_case(steps)
    summary = debug_case(case=case_steps, casename=casename, config=config)

    return Response(summary)


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
def run_testsuite(request):
    """
    :param request:
    :return:
    """
    pass


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

@api_view(['GET'])
def test(request):
    try:
        params = request.GET.get('id')
        data = request.data
        print(params)
        print('data获取'.format(data))
    except:
        print('fail')
    return Response('TEST')

