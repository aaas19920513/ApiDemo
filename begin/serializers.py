# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 22:21
# @Author  : tuihou
# @File    : serializers.py

from rest_framework import serializers
from .models import Project, Step, Case, Variables, API, Category, Config, Classify, TestSuite, Report, \
                    ReportCase, ReportDetail
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.validators import UniqueValidator
from django.db.models import Q


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目详情序列化

    """
    # 给project添加关联属性

    class Meta:
        model = Project
        fields = "__all__"


class ApiSerializer(serializers.ModelSerializer):

    """
        接口 序列化
    """
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    # name = serializers.CharField(label="接口名称", help_text="接口名", required=True, allow_blank=False,
    #                                  validators=[UniqueValidator(queryset=API.objects.all(), message="已经存在")])

    class Meta:
        model = API
        fields = "__all__"


class ApiSelectorSerializer(serializers.ModelSerializer):
    """
    api选择器序列化
    """

    class Meta:
        model = API
        fields = ['id', 'name', 'category']


class StepSerializer(serializers.ModelSerializer):
    """
    步骤序列化
    """

    class Meta:
        model = Step
        fields = "__all__"
        # depth = 1

    # api = ApiSerializer(read_only=True)


class CaseCopySerializer(WritableNestedModelSerializer):

    """
    case复制序列化
    """
    step = StepSerializer(many=True)

    class Meta:
        model = Case
        fields = "__all__"


class CaseSerializer(serializers.ModelSerializer):

    """
    case序列化
    """

    class Meta:
        model = Case
        fields = "__all__"

    # step = StepSerializer(many=True)
    # api = serializers.PrimaryKeyRelatedField(queryset=API.objects.all())
    create_user = serializers.CharField()
    update_user = serializers.CharField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    # def get_create_user(self, obj):
    #
    #     return


class CaseSelectorSerializer(serializers.ModelSerializer):

    """
    case选择器序列化
    """
    class Meta:
        model = Case
        fields = ['id', 'name']


class VariablesSerializer(serializers.ModelSerializer):

    """
    变量序列化
    """
    class Meta:
        model = Variables
        fields = "__all__"


class ConfigSerializer(serializers.ModelSerializer):

    """
     config序列化
    """
    class Meta:
        model = Config
        fields = "__all__"


class CategoryApiSerializer3(serializers.ModelSerializer):
    """
    三级类别api序列化
    """
    api = ApiSelectorSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'api']


class CategoryApiSerializer2(serializers.ModelSerializer):
    """
    二级类别api序列化
    """
    children = CategoryApiSerializer3(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'children']


class CategoryApiSerializer(serializers.ModelSerializer):
    """
    一级类别api序列化
    """
    children = CategoryApiSerializer2(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'children']


class CategoryCaseSerializer3(serializers.ModelSerializer):
    """
    三级类别case序列化name
    """
    case = CaseSelectorSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'case']


class CategoryCaseSerializer2(serializers.ModelSerializer):
    """
    二级类别case序列化
    """
    children = CategoryCaseSerializer3(many=True)

    class Meta:
        model = Category
        fields = ['id', 'label', 'children']


class CategoryCaseSerializer(serializers.ModelSerializer):
    """
    一级类别Case序列化
    """
    children = CategoryCaseSerializer2(many=True)

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


class SuiteDetailSerializer(serializers.ModelSerializer):
    """
    suite包含case详情序列化

    """
    case = CaseSerializer(many=True)

    class Meta:
        model = TestSuite
        fields = "__all__"


class SuiteSerializer(serializers.ModelSerializer):
    """
    suite序列化

    """

    class Meta:
        model = TestSuite
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


class ReportSerializer(serializers.ModelSerializer):
    """
    报告概要序列化
    """
    class Meta:
        model = Report
        fields = '__all__'


class ReportDetailSerializer(serializers.ModelSerializer):
    """
    step结果列化
    """
    class Meta:
        model = ReportDetail
        fields = '__all__'


class ReportCaseSerializer(serializers.ModelSerializer):
    """
    case结果序列化
    """
    # detail = ReportDetailSerializer(many=True)

    class Meta:
        model = ReportCase
        fields = '__all__'