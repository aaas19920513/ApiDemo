# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins, generics
from .serializers import ProjectSerializer3, CaseSerializer2, StepSerializer2, VariablesSerializer2
from .serializers2 import ProjectSer, StepSer, ConfigSer, CaseSer
from runner import models
from rest_framework.response import Response
from .utils import responce_dict, tools
from django.core import exceptions
from users.utils.MyAuth import Authentication


class ProjectView(viewsets.ModelViewSet):
    """
    项目视图
    """
    authentication_classes = []
    serializer_class = ProjectSerializer3
    queryset = models.Project.objects.all().order_by('-update_time')


class ProjectView2(GenericViewSet):

    queryset = models.Project.objects.all().order_by('-update_time')
    serializer_class = ProjectSerializer3
    authentication_classes = []

    def single(self, request, **kwargs):
        """
        得到单个项目相关统计信息
        """
        pk = kwargs.pop('pk')
        try:
            queryset = models.Project.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist:
            return Response(responce_dict.not_exict)
        serializer = self.get_serializer(queryset, many=False)
        # project_info = tools.get_project_detail(pk)
        # project_info.update(serializer.data)
        return Response(serializer.data)


class CaseView(viewsets.ModelViewSet):
    """
    case视图
    """
    authentication_classes = []
    serializer_class = CaseSerializer2
    queryset = models.Case.objects.all()


class StepView(viewsets.ModelViewSet):
    """
    casestep视图
    """
    authentication_classes = []
    serializer_class = StepSerializer2
    queryset = models.CaseStep.objects.all()


class VariablesView(viewsets.ModelViewSet):
    """
    变量视图
    """
    authentication_classes = []
    serializer_class = VariablesSerializer2
    queryset = models.Variables.objects.all()


class TestSuite(APIView):

    def post(self, request, **kwargs):
        project = models.Project.objects.filter(name=kwargs['name'])
        module = models.Module.objects.filter(project=project)

        return Response(module)


class ConfigView(viewsets.ModelViewSet):

    authentication_classes = []
    serializer_class = ConfigSer
    queryset = models.Config.objects.all()


class TestView(GenericViewSet):

    queryset = models.Project.objects.all().order_by('-update_time')
    serializer_class = ProjectSer
    authentication_classes = []

    def single(self, request, **kwargs):
        """
        得到单个项目相关统计信息
        """
        pk = kwargs.pop('pk')

        try:
            queryset = models.Project.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist:
            return Response(responce_dict.not_exict)
        serializer = self.get_serializer(queryset, many=False)
        # project_info = tools.get_project_detail(pk)
        # project_info.update(serializer.data)
        return Response(serializer.data)


class RunSingleTestCase(GenericViewSet):

    queryset = models.Case.objects.all().order_by()
    serializer_class = CaseSer
    authentication_classes = []

    def single(self, request, **kwargs):
        pk = kwargs.pop('pk')

        try:
            queryset = models.Case.objects.get(id=pk)
        except exceptions.ObjectDoesNotExist:
            return Response(responce_dict.not_exict)
        serializer = self.get_serializer(queryset, many=False)
        print(serializer.data)
        return Response(serializer.data)
