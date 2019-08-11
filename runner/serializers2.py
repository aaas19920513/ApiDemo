# -*- coding: utf-8 -*-
# @Time    : 2019/3/7 10:15
# @Author  : tuihou
# @File    : serializers2.py

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Project, Module, CaseStep, Case, Variables, Config, Debugtalk


class StepSer(WritableNestedModelSerializer):

    class Meta:
        model = CaseStep
        fields = ('pk', 'name', 'header', 'data', 'url', 'method', 'assert_response',)


class CaseSer(WritableNestedModelSerializer):

    step = StepSer(many=True)

    class Meta:
        model = Case
        fields = ('pk', 'name', 'step')


class ModuleSer(WritableNestedModelSerializer):

    case = CaseSer(many=True)

    class Meta:
        model = Module
        fields = ('pk', 'name', 'case')


class VariableSer(WritableNestedModelSerializer):

    class Meta:
        model = Variables
        fields = ('pk', 'key', 'value')


class ConfigSer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('pk', 'name', 'body', 'base_url')


class DebugTalkSerializer(serializers.ModelSerializer):
    """
    驱动代码序列化
    """

    class Meta:
        model = Debugtalk
        fields = ['id', 'code']


class ProjectSer(serializers.ModelSerializer):

    variables = VariableSer(many=True)
    module = ModuleSer(many=True)
    config = ConfigSer(many=True)

    class Meta:
        model = Project
        fields = ('pk', 'name', 'variables', 'config', 'module',)




