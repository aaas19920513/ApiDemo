# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 15:07
# @Author  : tuihou
# @File    : category.py

from begin import serializers
from begin import models
from rest_framework import status
from rest_framework import viewsets
from users.utils.response import JsonResponse
from rest_framework import filters
from django_filters import rest_framework
from users.utils import MyPaginatiion


def build_category_add_api(category_list):
    """
    构建目录包含api
    :param category_list:
    :return:
    """
    try:
        for category in category_list:
            cates_two = category['children']
            for cate_two in cates_two:
                cates_three = cate_two['children']
                for cate_three in cates_three:
                    cate_three['children'] = cate_three.pop('api')
                    api_list = cate_three['children']
                    for api in api_list:
                        api['label'] = api.pop('name')
        return category_list
    except:
        pass


def build_selector(category_list, celector):
    """
    构建选择器
    :param category_list:
    :param celector: 选择器种类 ，  such as : api ,  case
    :return:
    """
    try:
        for category in category_list:
            category['value'] = category.pop('id')
            if len(category['children']) > 0:
                cates_two = category['children']
                for cate_two in cates_two:
                    cate_two['value'] = cate_two.pop('id')
                    if len(cate_two['children']) > 0:
                        cates_three = cate_two['children']
                        for cate_three in cates_three:
                            cate_three['value'] = cate_three.pop('id')
                            if len(cate_three[celector]) >0:
                                cate_three['children'] = cate_three.pop(celector)
                                api_list = cate_three['children']
                                for api in api_list:
                                    api['label'] = api.pop('name')
                                    api['value'] = api.pop('id')
                            else:
                                cate_three.pop(celector)
                    else:
                        cate_two.pop('children')
            else:
                category.pop('children')
        return category_list
    except:
        pass


class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = MyPaginatiion.CustomPagination
    # filter_class = ServerFilter
    queryset = models.Category.objects.filter(category_type=1)
    serializer_class = serializers.CategoryApiSerializer
    permission_classes = ()
    filter_fields =()
    search_fields = ('name', 'category', 'id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 将api构建成category
        data = build_category_add_api(serializer.data)
        return JsonResponse(data=data, code=2001, msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=2001, msg="success", status=status.HTTP_200_OK)


class ApiCategoryViewSet(viewsets.ModelViewSet):
    """
    API选择器
    """
    pagination_class = MyPaginatiion.CustomPagination
    # filter_class = ServerFilter
    queryset = models.Category.objects.filter(category_type=1)
    serializer_class = serializers.CategoryApiSerializer
    permission_classes = ()
    filter_fields =()
    search_fields = ('name', 'category', 'id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 将api构建成category
        data = build_selector(serializer.data, 'api')
        return JsonResponse(data=data, code=2001, msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=2001, msg="success", status=status.HTTP_200_OK)


class CaseCategoryViewSet(viewsets.ModelViewSet):
    """
    case选择器
    """
    pagination_class = MyPaginatiion.CustomPagination
    # filter_class = ServerFilter
    queryset = models.Category.objects.filter(category_type=1)
    serializer_class = serializers.CategoryCaseSerializer
    permission_classes = ()
    filter_fields =()
    search_fields = ('name', 'category', 'id')
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 将case构建成category
        data = build_selector(serializer.data, 'case')
        return JsonResponse(data=data, code=2001, msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, code=2001, msg="success", status=status.HTTP_200_OK)