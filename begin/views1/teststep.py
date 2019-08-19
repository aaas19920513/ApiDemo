# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 17:14
# @Author  : tuihou
# @File    : teststep.py

from begin import serializers
from rest_framework import viewsets, mixins
from begin import models
from begin import filters
from users.utils.CustomView import CustomViewBase
from rest_framework import status
from users.utils.response import JsonResponse


class StepViewSet(CustomViewBase):
    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer
    filter_class = filters.StepFilter
    ordering = ('sequence',)


class StepCopyViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.StepSerializer
    queryset = models.Step.objects.all()

    def copy(self, request, **kwargs):
        try:
            pk = kwargs['pk']
            step_obj = models.Step.objects.get(id=pk)
            step_obj.id = None
            step_obj.name = step_obj.name + '--copy'
            step_obj.save()
            return JsonResponse(code=2001, msg='success', status=status.HTTP_200_OK, data=[])
        except:
            return JsonResponse(code=4004, msg='the id not found', status=status.HTTP_200_OK)
