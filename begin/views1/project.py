# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 15:28
# @Author  : tuihou
# @File    : project.py

from begin import serializers
from rest_framework import viewsets
from begin import models


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ConfigSerializer
    queryset = models.Project.objects.all()
