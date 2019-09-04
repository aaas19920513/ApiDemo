# -*- coding: utf-8 -*-
# @Time    : 2019/8/31 0:20
# @Author  : tuihou
# @File    : serializers.py
from tasks.models import Tasks
from rest_framework import serializers
from django_apscheduler.models import DjangoJob, DjangoJobExecution
import time


class TasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = '__all__'

    def validate_time_rule(self, attrs):
        if len(attrs) < 6:
            raise serializers.ValidationError('time_rule length must ==6')
        if not isinstance(attrs, list):
            raise serializers.ValidationError('time_rule type must be list')

    # def validate(self, data):
    #     """
    #     Check  the task start time must before the stop time.
    #     """
    #     if data['time_rule'][0] == '*':
    #         year = time.strftime("%Y", time.localtime())
    #         data['time_rule'][0] = year
    #         new_list = [time]
    #     if data['time_rule'] > data['end_date']:
    #         raise serializers.ValidationError("finish must occur after start")
    #     return data


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = DjangoJob
        fields = '__all__'