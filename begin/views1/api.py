# -*- coding: utf-8 -*-
# @Time    : 2019/6/2 10:51
# @Author  : tuihou
# @File    : api.py


from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins
from rest_framework import viewsets
from begin import models, serializers
from rest_framework.response import Response
from MyApi import responce_dict
from begin.filters import ApiFilter


class ApiViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """
    API操作视图
    """
    serializer_class = serializers.ApiSerializer
    queryset = models.API.objects.all()
    filter_class = ApiFilter
    search_fields = ('name', 'category', 'id')

    """使用默认分页器"""

    def list(self, request):
        """
        接口列表 {
            classify_id: int,
        }
        """
        category_id = request.query_params["category_id"]
        search = request.query_params["search"]
        queryset = self.get_queryset().filter(category_id=category_id)

        if search != '':
            queryset = queryset.filter(name__contains=search)

        # if classify_id != '':
        #     queryset = queryset.filter(relation=node)

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def add(self, request):
        """
        新增一个接口
        """

        api = request.data
        try:
            api_body = {
                'name': api['name'],
                'body': api['body'],
                'url': api['url'],
                'method': api['method'],
                'category_id': api['category_id']
            }
            obj = models.Category.objects.filter(id=api['category_id'])
            serialiezer = serializers.ApiSerializer(api_body)
            print(serialiezer)
            if serialiezer.is_valid():
                serialiezer.save()
            # models.API.objects.create(**api_body)
            return Response(responce_dict.success_dict)
        except:
            return Response(responce_dict.req_error)

    def update(self, request, **kwargs):
        """
        更新接口
        """
        try:
            # pk = kwargs['pk']
            # print(pk)
            api = request.data
            api_body = {
                'name': api['name'],
                'body': api['body'],
                'url': api['url'],
                'method': api['method'],
                'id': api['id'],
            }

            obj = models.API.objects.filter(id=api_body['id']).count()
            if obj == 1:
                obj.update(**api_body)
                return Response(responce_dict.success_dict)
            else:
                return Response(responce_dict.not_exict)
        except ObjectDoesNotExist:
            return Response(responce_dict.not_exict)

    #
    # def copy(self, request, **kwargs):
    #     """
    #     pk int: test id
    #     {
    #         name: api name
    #     }
    #     """
    #     pk = kwargs['pk']
    #     name = request.data['name']
    #     api = models.API.objects.get(id=pk)
    #     body = eval(api.body)
    #     body["name"] = name
    #     api.body = body
    #     api.id = None
    #     api.name = name
    #     api.save()
    #     return Response(response.API_ADD_SUCCESS)
    #
    #
    # def delete(self, request, **kwargs):
    #     """
    #     删除一个接口 pk
    #     删除多个
    #     [{
    #         id:int
    #     }]
    #     """
    #
    #     try:
    #         if kwargs.get('pk'):  # 单个删除
    #             models.API.objects.get(id=kwargs['pk']).delete()
    #         else:
    #             for content in request.data:
    #                 models.API.objects.get(id=content['id']).delete()
    #
    #     except ObjectDoesNotExist:
    #         return Response(response.API_NOT_FOUND)
    #
    #     return Response(response.API_DEL_SUCCESS)
    #
    # def single(self, request, **kwargs):
    #     """
    #     查询单个api，返回body信息
    #     """
    #     try:
    #         api = models.API.objects.get(id=kwargs['pk'])
    #     except ObjectDoesNotExist:
    #         return Response(response.API_NOT_FOUND)
    #
    #     parse = Parse(eval(api.body))
    #     parse.parse_http()
    #
    #     resp = {
    #         'id': api.id,
    #         'body': parse.testcase,
    #         'success': True,
    #     }
    #
    #     return Response(resp)


class ApiViewSet2(viewsets.ModelViewSet):
    '''
           retrieve:
               Return a api instance.

           list:
               Return all api,ordered by most recent joined.

           create:
               Create a new api

           delete:
               Remove a existing api.

           partial_update:
               Update one or more fields on a existing api.

           update:
               Update a api.
       '''

    queryset = models.API.objects.all()
    serializer_class = serializers.ApiSerializer
    filter_class = ApiFilter
    search_fields = ('name', 'category', 'url')

from users.utils.CustomView import CustomViewBase
from users.utils.MyPaginatiion import CustomPagination


class ApiViewSet3(CustomViewBase):
    '''
           retrieve:
               Return a api instance.

           list:
               Return all api,ordered by most recent joined.

           create:
               Create a new api

           delete:
               Remove a existing api.

           partial_update:
               Update one or more fields on a existing api.

           update:
               Update a api.
       '''

    queryset = models.API.objects.all()
    serializer_class = serializers.ApiSerializer
    filter_class = ApiFilter
    search_fields = ('name', 'category', 'url')