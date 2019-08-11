# -*- coding: utf-8 -*-
# @Time    : 2019/6/15 15:20
# @Author  : tuihou
# @File    : config.py

from begin import serializers
from rest_framework import viewsets
from begin import models


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = models.Config.objects.all()
    serializer_class = serializers.ConfigSerializer