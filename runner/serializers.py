# -*- coding: utf-8 -*-
# @Time    : 2019/3/2 22:32
# @Author  : tuihou
# @File    : serializers.py

from rest_framework import serializers
from .models import Project, Module, CaseStep, Case, Variables, Debugtalk


class ProjectSerializer3(serializers.ModelSerializer):
    """
    项目详情序列化

    """
    # 给project添加关联属性
    module = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='module-detail')
    variables = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='variables-detail')

    class Meta:
        model = Project
        fields = ('id', "name", 'developer', 'tester', 'status', 'description', 'variables', 'module')


class CaseSerializer2(serializers.ModelSerializer):

    step = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='step-detail')

    class Meta:
        model = Case
        fields = ('id', 'module', 'name', 'description', 'step')


class StepSerializer2(serializers.ModelSerializer):

    class Meta:
        model = CaseStep
        fields = ('id', 'name', 'url', 'header', 'data', 'method', 'case', 'assert_response', 'description')


class VariablesSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Variables
        fields = ('id', 'project', 'key', 'value')


class ProjectSerializer2(serializers.ModelSerializer):
    """
    项目详情序列化

    """
    class Meta:
        model = Project
        fields = ('id', "name", 'developer', 'tester', 'status', 'description', 'module', '')
        depth = 5