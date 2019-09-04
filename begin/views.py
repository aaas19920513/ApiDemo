from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins, generics
from .serializers import ApiSerializer
from begin import models
from rest_framework.response import Response
from django.core import exceptions
import json
from .utils.prepare import build_case, build_case_by_id
from .utils.parse import debug_cases,  debug_case
from django.forms.models import model_to_dict
from rest_framework import status
from users.utils.response import JsonResponse
from django.core import serializers as parse
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
# from begin.utils.tools import send_email
from django.shortcuts import HttpResponse
import time
import django.dispatch
from django.dispatch import receiver
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED

# Create your views here.

# from .views1 import tasks
# import logging
# logger = logging.getLogger('job')
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), 'default')
#
#
# def job_listener(Event):
#     job = scheduler.get_job(Event.job_id)
#     if not Event.exception:
#         print("jobname={}|jobtrigger={}|jobtime={}|retval={}|jobID{}".format(job.name, job.trigger,
#                     Event.scheduled_run_time, Event.retval, job.id))
#     else:
#         print("jobname=%s|jobtrigger=%s|errcode=%s|exception=[%s]|traceback=[%s]|scheduled_time=%s", job.name,
#                      job.trigger, Event.code,
#                      Event.exception, Event.traceback, Event.scheduled_run_time)
#
#
# def test_add_task(request):
#     if request.method == 'POST':
#         # content = json.loads(request.body.decode())  # 接收参数
#         print('发送邮件')
#         try:
#             # start_time = content['start_time']  # 用户输入的任务开始时间, '10:00:00'
#             # start_time = start_time.split(':')
#             # hour = int(start_time[0])
#             # minute = int(start_time[1])
#             # second = int(start_time[2])
#             # s = content['s']  # 接收执行任务的各种参数
#             # d = content['d']
#             # 创建任务
#             # scheduler.add_job(tasks.test, trigger='date', replace_existing=True, run_date=datetime(2019, 9, 3, 13, 4, 00), name='test_for_name')
#             # scheduler.add_job(tasks.test,id='idtest33', trigger='interval', seconds=666, name='test666')
#             scheduler.add_job(tasks.test, trigger='cron', id='666966t',
#                               seconds=11)
#             # scheduler.add_job(tasks.test, start_date=datetime(2019, 9, 3, 12, 4, 00), end_date=datetime(2020, 9, 3, 13, 4, 00), trigger='cron', month=11, day=1, hour=23, minute=00)
#
#             scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR| EVENT_JOB_MISSED)
#
#             code = '200'
#             message = 'success'
#         except Exception as e:
#             code = '400'
#             message = e
#         back = {
#             'code': code,
#             'message': message
#         }
#         return HttpResponse('test')
#
# # from datetime import date
# # @register_job(scheduler, "date", run_date=date(2019, 9, 6))
# # def test_job():
# #     time.sleep(4)
# #     print("I'm a test job!")
# #     # raise ValueError("Olala!")
#
# def ttt():
#     print('35etststst')
# register_events(scheduler)
# scheduler.start()
#
#
# class TasksView(APIView):
#
#     def post(self, request, **kwargs):
#         try:
#             data = request.data
#             type_timer = data['type']
#             func = data['func']
#             time_data = data['time']
#             s = data['args']
#             d = data['kwargs']
#             hour = time_data['']
#             minute = time_data['']
#             second = time_data['']
#             day = time_data['day']
#             scheduler.add_job(func, trigger=type_timer, hour=hour, minute=minute, second=second, args=s, kwargs=d)
#
#         except:
#             return JsonResponse(status=status.HTTP_404_NOT_FOUND, msg='服务器开小差了', data=[], code=4001)
#         return JsonResponse(status=status.HTTP_201_CREATED, msg='success', data=[], code=2001)
#
#     def get(self, request, **kwargs):
#         try:
#             # id = kwargs['pk']
#             data = scheduler.get_jobs()
#             da = scheduler.print_jobs()
#             print(da)
#             print(data)
#             # data = json.loads(data)
#         except Exception as E:
#             print(E)
#             return JsonResponse(status=status.HTTP_404_NOT_FOUND, msg='服务器开小差了', data=[], code=4001)
#         return JsonResponse(status=status.HTTP_201_CREATED, msg='success', data=[data], code=2001)
#
#     def put(self, request,**kwargs):
#         try:
#             id = kwargs['pk']
#             data = scheduler.get_job(job_id=id)
#         except:
#             return JsonResponse(status=status.HTTP_404_NOT_FOUND, msg='服务器开小差了', data=[], code=4001)
#         return JsonResponse(status=status.HTTP_201_CREATED, msg='success', data=[data], code=2001)
