# -*- coding: utf-8 -*-
# @Time    : 2019/7/7 15:48
# @Author  : tuihou
# @File    : filters.py


from django_filters import rest_framework as filters
from begin.models import API, Case, Step, ReportCase
from django.db.models import Q


class ApiFilter(filters.FilterSet):
    """
    接口过滤类
    """
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.NumberFilter(field_name="category", method='category_filter')

    def category_filter(self, queryset, name, value):
        # 不管当前点击的是一级目录二级目录还是三级目录。
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = API
        fields = ['name', 'id', 'category']


class CaseFilter(filters.FilterSet):
    """
    case 过滤类
    """
    category = filters.NumberFilter(field_name="category", method='category_filter')
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    def category_filter(self, queryset, name, value):
        # 不管当前点击的是一级目录二级目录还是三级目录。
        return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Case
        fields = ['id', 'name', 'category', 'api']


class StepFilter(filters.FilterSet):
    """
    step 过滤类
    """

    class Meta:
        model = Step
        fields = ['id', 'case']


class ReportCaseFilter(filters.FilterSet):
    """
    ReportCase 过滤类
    """
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ReportCase
        fields = ['id', 'name', 'report', 'result']