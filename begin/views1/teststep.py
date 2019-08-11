# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 17:14
# @Author  : tuihou
# @File    : teststep.py

from begin import serializers
from rest_framework import viewsets
from begin import models
from begin import filters
from users.utils.CustomView import CustomViewBase


class StepViewSet(CustomViewBase):
    queryset = models.Step.objects.all()
    serializer_class = serializers.StepSerializer
    filter_class = filters.StepFilter