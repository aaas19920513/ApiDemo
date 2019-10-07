# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 17:34
# @Author  : tuihou
# @File    : Case.py
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from begin import serializers
from rest_framework import viewsets
from begin import models
from users.utils.CustomView import CustomViewBase
from users.utils import MyPaginatiion
from begin.filters import CaseFilter
from rest_framework import status
from users.utils.response import JsonResponse
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from begin.utils.prepare import build_case_by_id
from begin.utils.parse import debug_cases, create_report_obj
from django.core import serializers as parse
import json
import logging
logger = logging.getLogger('case')


class CaseViewSet(CustomViewBase):
    # permission_classes = [IsAuthenticated]
    pagination_class = MyPaginatiion.CustomPagination
    serializer_class = serializers.CaseSerializer
    queryset = models.Case.objects.all()
    filter_class = CaseFilter
    search_fields = ('name', 'category', 'api',)
    ordering = ('-update_time',)

    @action(methods=['delete'], detail=False)
    def deleteLots(self, request, *args, **kwargs):
        """
        批量删除
        :param request: {'ids': []}
        :param args:
        :param kwargs:
        :return:
        """
        delete_id = request.query_params.get('ids', None)
        if not delete_id:
            return JsonResponse(code=4004, msg='服务器开小差了', status=status.HTTP_404_NOT_FOUND)
        # ids = delete_id.strip('[]')
        # for i in ids.split(','):
        #     get_object_or_404(models.Case, pk=int(i)).delete()
        models.Case.objects.extra(where=["id IN (" + delete_id + ")"]).delete()
        logger.info('-'*10 + ('删除case by:{} '.format(request.user)) + '-'*10)
        return JsonResponse(status=status.HTTP_200_OK, code=2001, msg='delete success')

    @action(methods=['post'], detail=False)
    def runById(self, request, *args, **kwargs):
        """
        批量运行
        :param request: {'ids':[], config:''}
        :param args:
        :param kwargs:
        :return:
        """
        cases = []
        data = request.data
        config = data['config']
        case_id_list = data['ids']
        if not case_id_list:
            return JsonResponse(code=4004, msg='服务器开小差了', status=status.HTTP_404_NOT_FOUND)

        if not isinstance(case_id_list, list):
            case_id_list = [case_id_list, ]

        for case_id in case_id_list:
            steps_query = models.Step.objects.filter(case_id=case_id)
            if not steps_query:
                return JsonResponse(code=2001, msg='这个{}未添加步骤'.format(case_id), status=status.HTTP_404_NOT_FOUND)
            case = build_case_by_id(case_id)
            cases.append(case)

        summary = debug_cases(cases, config=config)
        try:
            create_report_obj(summary)
        except:
            return JsonResponse(status=status.HTTP_200_OK, code=4004, msg='生成报告失败', data=[])
        return JsonResponse(status=status.HTTP_200_OK, code=2001, msg='报告生成中', data=[])

    @action(methods=['post'], detail=False)
    def runSuite(self, request, *args, **kwargs):
        """
        运行suite
        :param request: {'id':'', config:''}
        :param args:
        :param kwargs:
        :return:
        """
        try:
            cases = []
            data = request.data
            config = data['config']
            suite_id = data['id']
            suite_obj = models.TestSuite.objects.get(id=suite_id)
            case_obj = suite_obj.case.all().values('id')
            case_id_list_obj = map(lambda x: x['id'], case_obj)
            case_id_list = [case for case in case_id_list_obj]
        except:
            return JsonResponse(code=4004, msg='服务器开小差了', status=status.HTTP_404_NOT_FOUND)

        if not isinstance(case_id_list, list):
            case_id_list = [case_id_list, ]
        #
        for case_id in case_id_list:
            steps_query = models.Step.objects.filter(case_id=case_id)
            if not steps_query:
                return JsonResponse(code=2001, msg='这个{}未添加步骤'.format(case_id), status=status.HTTP_404_NOT_FOUND)
            case = build_case_by_id(case_id)
            cases.append(case)
        summary = debug_cases(cases, config=config)
        # report = create_report_obj(summary, suite_obj)
        try:
            create_report_obj(summary, suite_id)
        except:
            return JsonResponse(status=status.HTTP_200_OK, code=4004, msg='生成报告失败', data=[])
        return JsonResponse(status=status.HTTP_200_OK, code=2001, msg='报告生成中', data=[])

    @action(methods=['get'], detail=False)
    def getLots(self, request, *args, **kwargs):
        """
        批量查询
        :param request: {'ids': []}
        :param args:
        :param kwargs:
        :return:
        """
        try:
            ids_obj = request.query_params.get('ids', None)
            queryset = models.Case.objects.in_bulk(ids_obj)
            ser = self.serializer_class(instance=queryset.values(), many=True)
        except:
            return JsonResponse(code=4004, msg='服务器开小差了', status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(status=status.HTTP_200_OK, code=2001, msg='success', data=ser.data)


class CaseCopyViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.CaseCopySerializer
    queryset = models.Case.objects.all()

    def copy(self, request, **kwargs):
        try:
            pk = kwargs['pk']
            case_obj = models.Case.objects.get(id=pk)
            if not case_obj:
                return JsonResponse(code=4004, msg='this case not exist', status=status.HTTP_200_OK)

            steps = models.Step.objects.filter(case_id=pk)
            if not steps:
                return JsonResponse(code=2001, msg='this case no caseStep, please add it', status=status.HTTP_200_OK)

            case_obj.id = None
            case_obj.name = case_obj.name + '--copy'
            case_obj.save()

            steps = models.Step.objects.filter(case_id=pk)
            for step in steps:
                step.id = None
                step.case = case_obj
            #     step.save()
            models.Step.objects.bulk_create(steps)
            return JsonResponse(code=2001, msg='success', status=status.HTTP_200_OK, data=[])
        except:
            return JsonResponse(code=4004, msg='sorry,服务器开小差', status=status.HTTP_200_OK)

