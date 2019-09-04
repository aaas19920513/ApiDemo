# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 18:22
# @Author  : tuihou
# @File    : urls.py

from django.urls import path
from . import views, view_bk

# app_name = 'users'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='注册'),
    # jwt
    # path('register2', view_bk.UserViewSet.as_view({'get':'retrieve', 'post': 'create'}), name='注册'),
    path('login', views.LoginView.as_view(), name='登录'),
    path('user/info', views.UserInfoView.as_view(),  name='UserInfo')
]