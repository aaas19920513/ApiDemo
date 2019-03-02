# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 16:20
# @Author  : tuihou
# @File    : serializers.py


from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInfo
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.HyperlinkedModelSerializer):

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserInfo.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    class Meta:
        model = UserInfo
        fields = ("username", "password", 'type')


