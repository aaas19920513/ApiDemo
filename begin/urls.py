# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 22:49
# @Author  : tuihou
# @File    : urls.py


from django.urls import path
from begin import views
from .views1 import api


urlpatterns = [
    path('case/<int:pk>/', views.RunSingleTestCase.as_view({"get": 'single'})),
    # path('interface/<int:pk>/', views.RunSingleApi.as_view({"get": 'single'})),
    path('run/api/', views.run_api),
    path('run/case/', views.run_case),
    path('interface/', api.ApiViewSet.as_view({"get": 'list', "post": 'add', "patch": 'update'})),
    path('run/case_id_list/', views.run_case_by_id),
    path('bbbb', views.test),
]
