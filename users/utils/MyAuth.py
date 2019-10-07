# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 22:15
# @Author  : tuihou
# @File    : MyAuth.py

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from users import models
from users.utils.response_dict import auth_failed, auth_out_of_date
import datetime
import pytz
from django.conf import settings


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        """
        用户认证，如果验证成功后返回元组： (用户,用户Token)
        :param request:
        :return:
            None,表示跳过该验证；
                如果跳过了所有认证，默认用户和Token和使用配置文件进行设置
                self._authenticator = None
                if api_settings.UNAUTHENTICATED_USER:
                    self.user = api_settings.UNAUTHENTICATED_USER() # 默认值为：匿名用户
                else:
                    self.user = None

                if api_settings.UNAUTHENTICATED_TOKEN:
                    self.auth = api_settings.UNAUTHENTICATED_TOKEN()# 默认值为：None
                else:
                    self.auth = None
            (user,token)表示验证通过并设置用户名和Token；
            AuthenticationFailed异常
        """
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed(auth_failed)

        end = datetime.datetime.now()
        start = token_obj.create_time
        time_difference = (end - start).seconds
        print(time_difference)
        if time_difference > settings.TIME_DIFFERENCE:
            raise exceptions.AuthenticationFailed(auth_out_of_date)
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        # return 'Basic realm=api'
        pass