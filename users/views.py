from rest_framework.views import APIView
from users.serializers import UserRegSerializer, UserDetailSerializer
from users import models
from rest_framework.response import Response
from django.http import JsonResponse
from users.utils import MyToken, response_dict
from users.utils.MyAuth import Authentication
from MyApi import tools
import os
from django.contrib.auth import get_user_model
import logging
from django.conf import settings
from django.contrib.auth.hashers import make_password

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
User = get_user_model()
logger = logging.getLogger('User')


class RegisterView(APIView):
    # 为空代表不需要认证
    authentication_classes = []

    def post(self, request):
        try:
        #     username = request.data['username']
            password = request.data['password']
        except ValueError as E:
            return Response(response_dict.miss_value_dict)
        # if models.UserProfile.objects.filter(username=username).first():
        #     return Response(response_dict.register_failed)
        # 解决QueryDict不能修改的问题
        request_data = request.data.copy()
        request_data['password'] = tools.hash_code(password)
        serializer = UserRegSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(response_dict.success_dict)


class LoginView(APIView):

    authentication_classes = []

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except ValueError as E:
            return Response(response_dict.miss_value_dict)
        user = User.objects.filter(username=username, password=tools.hash_code(password)).first()
        if user:
            token = MyToken.get_random_token(username)
            models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
            response_dict.token_dict['token'] = token
            response_dict.token_dict['username'] = username
            return Response(response_dict.token_dict)
        return Response(response_dict.login_failed)


class UserInfoView(APIView):
    authentication_classes = [Authentication]

    def get(self, request):
        try:
            token = request.query_params['token']
            token_obj = models.UserToken.objects.filter(token=token).first()
            if token_obj:
                user = token_obj.user
                username = (str(user))
                ret = {
                    'code': 2001,
                    'msg': 'success',
                    'username': username
                }
                return JsonResponse(ret)
        except:
            return Response(response_dict.miss_value_dict)


from .utils import CustomView


class UserViewSet(CustomView.CustomViewBase):

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


from django.shortcuts import HttpResponse
import time
import django.dispatch
from django.dispatch import receiver

# Create your views here.

# 定义一个信号
work_done = django.dispatch.Signal(providing_args=['path', 'time'])


def create_signal(request):
    url_path = request.path
    print("我已经做完了工作。现在我发送一个信号出去，给那些指定的接收器。")

    # 发送信号，将请求的IP地址和时间一并传递过去
    work_done.send(create_signal, path=url_path, time=time.strftime("%Y-%m-%d %H:%M:%S"))
    return HttpResponse("200,ok")


@receiver(work_done, sender=create_signal)
def my_callback(sender, **kwargs):
    print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))



from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from . import models
from django.shortcuts import render, get_object_or_404
class FileView(APIView):

    def post(self, request):
        """
        接收文件并保存
        """
        file = request.FILES['file']

        if models.FileBinary.objects.filter(name=file.name).first():
            return Response("test")

        body = {
            "name": file.name,
            "body": file.file.read(),
            "size": 55
        }

        models.FileBinary.objects.create(**body)

        return Response('testst')

    def get(self, request, **kwargs):
        pk = kwargs.get('pk',  None)
        print(kwargs)
        binfile = get_object_or_404(models.FileBinary, pk=pk)
        print(binfile.name)
        resp = HttpResponse(binfile.body, content_type='application/octet-stream')
        resp['Content-Disposition'] = 'attachment; filename="%s"' % binfile.name
        return resp


from django.views.decorators.cache import cache_page
import time


@cache_page(15)  # 超时时间为15秒
def test(request):
    t = time.localtime()
    return HttpResponse(t)