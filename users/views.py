from rest_framework.views import APIView
from users.serializers import UserRegSerializer
from users import models
from rest_framework.response import Response
from users.utils import MyToken, response_dict
from users.utils.myauth import Authentication
from rest_framework.authentication import BaseAuthentication
import hashlib


# 加点盐
def hash_code(s, salt='tuihou'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


class RegisterView(APIView):
    # 为空代表不需要认证
    authentication_classes = []

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response(response_dict.miss_value_dict)
        if models.UserInfo.objects.filter(username=username).first():
            return Response(response_dict.register_failed)
        # 解决QueryDict不能修改的问题
        request_data = request.data.copy()
        request_data['password'] = hash_code(password)
        serializer = UserRegSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_dict.success_dict)
        else:
            return Response(response_dict.miss_value_dict)


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response(response_dict.miss_value_dict)
        user = models.UserInfo.objects.filter(username=username, password=hash_code(password)).first()
        if user:
            token = MyToken.get_random_token(username)
            models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
            response_dict.token_dict['token'] = token
            response_dict.token_dict['username'] = username
            return Response(response_dict.token_dict)
        else:
            return Response(response_dict.login_failed)


class OrderView(APIView):

    authentication_classes = [Authentication]

    def get(self,request):

        return Response('test')