# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 22:21
# @Author  : tuihou
# @File    : serializers.py

from rest_framework import serializers
from .models import Project, Step, Case, Variables, API, Category, Config, Classify
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.validators import UniqueValidator
from django.db.models import Q


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目详情序列化

    """
    # 给project添加关联属性
    module = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='module-detail')
    variables = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='variables-detail')

    class Meta:
        model = Project
        fields = "__all__"


class ApiSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    # name = serializers.CharField(label="接口名称", help_text="接口名", required=True, allow_blank=False,
    #                                  validators=[UniqueValidator(queryset=API.objects.all(), message="用户已经存在")])

    class Meta:
        model = API
        fields = "__all__"


class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = Step
        fields = "__all__"
        # depth = 1

    # api = ApiSerializer(read_only=True)


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = "__all__"

    # step = StepSerializer(many=True)
    api = serializers.PrimaryKeyRelatedField(queryset=API.objects.all())
    create_user = serializers.CharField(default=serializers.CurrentUserDefault())
    update_user = serializers.CharField(default=serializers.CurrentUserDefault())


class VariablesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variables
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = "__all__"


class ApiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品三级类别序列化
    """
    api = ApiSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'api']


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品二级类别序列化
    """
    children = CategorySerializer3(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'children']


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    children = CategorySerializer2(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'children']


class ProjectSerializer2(serializers.ModelSerializer):
    """
    项目详情序列化

    """
    class Meta:
        model = Project
        fields = "__all__"


class ClassifySerializer(serializers.ModelSerializer):

    """
    分类序列化
    """

    class Meta:
        model = Classify
        fields = "__all__"


class TestSerializer(serializers.Serializer):

    api = serializers.PrimaryKeyRelatedField(queryset=API.objects.all())
    name = serializers.CharField(max_length=50)
    runFlag = serializers.IntegerField()
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # project = serializers.CharField()

    class Meta:
        model = Case
    #     fields = '__all__'

    def validated_name(self, value):
        if 'tttt' not in value.lower():
            raise serializers.ValidationError('this is test for validated')
        return value

    def create(self, validated_data):
        # user = self.context["request"].user
        return Case.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.runFlag = validated_data.get('runFlag', instance.runFlag)
    #     instance.save()
    #     return instance




