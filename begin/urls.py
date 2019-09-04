# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 22:49
# @Author  : tuihou
# @File    : urls.py


from django.urls import path
from begin import views
from .views1 import teststep, case, run, tasks


urlpatterns = [
    path('step/copy/<int:pk>', teststep.StepCopyViewSet.as_view({"post": 'copy'})),
    path('case/copy/<int:pk>', case.CaseCopyViewSet.as_view({"post": 'copy'})),
    path('run/case', run.RunCaseByBodyView.as_view()),
    # path('tasksjob/<int:pk>', views.TasksView.as_view()),
    # path('tasks2', tasks.TasksResultsView2.as_view()),
    # path('tasks2/<int:pk>', tasks.TasksResultsView2.as_view()),
    # path('ttt/<int:pk>', tasks.TasksVIew.as_view()),
    # path('test2', views.test_add_task),
]
