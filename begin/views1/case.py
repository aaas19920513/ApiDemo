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


class CaseViewSet(CustomViewBase):
    pagination_class = MyPaginatiion.CustomPagination
    serializer_class = serializers.CaseSerializer
    queryset = models.Case.objects.all()
    filter_class = CaseFilter
    search_fields = ('name', 'category', 'api')

