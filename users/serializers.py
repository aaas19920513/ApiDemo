# -*- coding: utf-8 -*-
# @Time    : 2019/2/28 16:20
# @Author  : tuihou
# @File    : serializers.py

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
# from .models import UserInfo
from .models import UserProfile
User = get_user_model()
from django.utils.timezone import now
from MyApi import tools


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = UserProfile
        exclude = ("password",)


class UserRegSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True, allow_blank=False, label="用户名", max_length=16, min_length=5,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
                                     error_messages={
                                         "blank": "用户名不允许为空",
                                         "required": "请输入用户名",
                                         "max_length": "用户名长度最长为16位",
                                         "min_length": "用户名长度至少为6位"
                                     })

    email = serializers.EmailField(required=True, allow_blank=False, min_length=6,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="邮箱已被使用")])

    password = serializers.CharField(
        write_only=True, min_length=6, error_messages={
            'blank': '密码不能为空',
            'required': '请输入密码',
            'min_length': '密码最少6个字符',
            'max': '密码最多18位',
        },
    )

    days_since_joined = serializers.SerializerMethodField()
    # second_password = serializers.CharField(source='user.confirm_password')

    class Meta:
        model = User
        fields = ("password", "username", "email")
        read_only_fields = ("username",)

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('this is test for validated')
        return value

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


class User2Serializer(serializers.Serializer):
    email = serializers.EmailField()
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.created = validated_data.get('created', instance.created)
        return instance