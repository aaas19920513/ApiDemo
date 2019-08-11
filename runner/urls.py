# -*- coding: utf-8 -*-
# @Time    : 2019/3/3 17:00
# @Author  : tuihou
# @File    : urls.py

from django.urls import path
from . import views


app_name = 'runner'
urlpatterns = [

    path('runcase/<int:pk>/', views.RunSingleTestCase.as_view({"get": 'single'})),
    path('test/<int:pk>/', views.TestView.as_view({"get": 'single'})),
    path('test/?<int:pk>/', views.TestView.as_view({"get": 'single'})),
    path('project/', views.ProjectView.as_view({"get": 'list', 'post': 'create'}),),
    path('project/<int:pk>/', views.ProjectView.as_view({"get": 'retrieve', 'delete': 'destroy',
                                                          'put': 'update', 'patch': 'partial_update'})),
    path('project2/<int:pk>/', views.ProjectView2.as_view({"get": 'single'})),
    # path('Variables/', views.VariablesView.as_view())
]

