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