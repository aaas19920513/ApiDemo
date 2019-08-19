# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 22:49
# @Author  : tuihou
# @File    : urls.py


from django.urls import path
from begin import views
from .views1 import teststep, case


urlpatterns = [
    path('step/copy/<int:pk>/', teststep.StepCopyViewSet.as_view({"post": 'copy'})),
    path('case/copy/<int:pk>/', case.CaseCopyViewSet.as_view({"post": 'copy'})),
    path('run/case', views.RunCaseByBodyView.as_view()),
    path('run/case_id_list/', views.run_case_by_id),
]
