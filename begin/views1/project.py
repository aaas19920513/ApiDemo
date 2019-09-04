# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 15:28
# @Author  : tuihou
# @File    : project.py

from begin import serializers
from rest_framework import viewsets
from begin import models
from users.utils.CustomView import CustomViewBase
from users.utils.response import JsonResponse
from rest_framework.decorators import action
from rest_framework import status
from django.forms.models import model_to_dict
from django.core import serializers as parse


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()


class SuiteDetailViewSet(CustomViewBase):
    serializer_class = serializers.SuiteDetailSerializer
    queryset = models.TestSuite.objects.all()


class SuiteViewSet(CustomViewBase):
    serializer_class = serializers.SuiteSerializer
    queryset = models.TestSuite.objects.all()