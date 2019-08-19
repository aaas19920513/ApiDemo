# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 17:34
# @Author  : tuihou
# @File    : Case.py
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
from begin.utils.parse import debug_cases


class CaseViewSet(CustomViewBase):
    pagination_class = MyPaginatiion.CustomPagination
    serializer_class = serializers.CaseSerializer
    queryset = models.Case.objects.all()
    filter_class = CaseFilter
    search_fields = ('name', 'category', 'api')
    ordering = ('-update_time',)

    @action(methods=['delete'], detail=False)
    def delete_lots(self, request, *args, **kwargs):
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
        ids = delete_id.strip('[]')
        for i in ids.split(','):
            get_object_or_404(models.Case, pk=int(i)).delete()
        return JsonResponse(status=status.HTTP_200_OK, code=2001, msg='delete success')

    @action(methods=['post'], detail=False)
    def run_by_id(self, request, *args, **kwargs):
        """
        批量运行
        :param request: {'ids':[], config:''}
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        config = data['config']
        case_id_list = data['ids']
        if not case_id_list:
            return JsonResponse(code=4004, msg='服务器开小差了', status=status.HTTP_404_NOT_FOUND)
        if not isinstance(case_id_list, list):
            case_id_list = [case_id_list, ]
        case = build_case_by_id(case_id_list)
        summary = debug_cases(case, config=config)
        return JsonResponse(status=status.HTTP_200_OK, code=2001, msg='delete success', data=summary)


class CaseCopyViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.CaseCopySerializer
    queryset = models.Case.objects.all()

    def copy(self, request, **kwargs):
        try:
            pk = kwargs['pk']
            case_obj = models.Case.objects.get(id=pk)
            case_obj.id = None
            case_obj.name = case_obj.name + '--copy'
            case_obj.save()

            steps = models.Step.objects.filter(case_id=pk)
            if steps:
                for step in steps:
                    step.id = None
                    step.case = case_obj
                    step.save()
            return JsonResponse(code=2001, msg='success', status=status.HTTP_200_OK, data=[])
        except:
            return JsonResponse(code=4004, msg='the id not found', status=status.HTTP_200_OK)

