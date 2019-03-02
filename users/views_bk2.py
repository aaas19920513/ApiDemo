# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 18:08
# @Author  : tuihou
# @File    : views_bk2.py


from rest_framework import viewsets, mixins, status
from users.serializers import UserRegSerializer
from users import models
from rest_framework.response import Response


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = UserRegSerializer
    queryset = models.UserInfo.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        # payload = jwt_payload_handler(user)
        # print(payload)
        # re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        re_dict['code'] = 1001
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

# class RegisterViewSet(viewsets.ModelViewSet):
#
#     queryset = models.UserInfo.objects.all()
#     serializer_class = UserRegSerializer


from users.utils.CustomView import CustomViewBase
from users.utils.response import JsonResponse


class BatchLoadView(CustomViewBase):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserRegSerializer

    def list(self, request, *args, **kwargs):
        return JsonResponse(code=2000, data=[], msg="testings44444444444444444444444")