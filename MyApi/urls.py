"""MyApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from tasks import views as TasksView
from rest_framework_jwt.views import obtain_jwt_token
from begin.views1 import api, category, config, project, teststep, case, report
# 删除url尾部斜杠 trailing_slash=False
router = routers.DefaultRouter(trailing_slash=False)
from users import views as UserView
# swagger1
from rest_framework.schemas import get_schema_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
# schema_view = get_schema_view(title='API', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])
#
# # swagger2
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
#
# schema_view2 = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )
router.register('api/usertest', viewset=UserView.UserViewSet, base_name='user')
router.register('api/interface', viewset=api.ApiViewSet3, base_name='api')
router.register('api/category', viewset=category.CategoryViewSet, base_name='category')
router.register('api/config', viewset=config.ConfigViewSet, base_name='config')
router.register('api/project', viewset=project.ProjectViewSet, base_name='project')
router.register('api/suiteDetail', viewset=project.SuiteDetailViewSet, base_name='suiteDetail')
router.register('api/suite', viewset=project.SuiteViewSet, base_name='suite')
router.register('api/step', viewset=teststep.StepViewSet, base_name='step')
router.register('api/case', viewset=case.CaseViewSet, base_name='case')
router.register('api/apiSelector', viewset=category.ApiCategoryViewSet, base_name='apiSelector')
router.register('api/caseSelector', viewset=category.CaseCategoryViewSet, base_name='caseSelector')
router.register('api/report', viewset=report.ReportViewSet, base_name='report')
router.register('api/reportCase', viewset=report.ReportCaseViewSet, base_name='reportCase')
router.register('api/reportDetail', viewset=report.ReportDetailViewSet, base_name='reportDetail')
router.register('api/tasks', viewset=TasksView.TasksViewSet, base_name='tasks')

from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html"), name="index"),
    # path('api/', include('chat.urls')),
    path('api/', include('begin.urls')),
    path('api/', include('users.urls')),
    path('api/', include('tasks.urls')),
    path('admin/', admin.site.urls),
    #jwt的token认证
    path('auth/', obtain_jwt_token),
    path('', include(router.urls)),
    # re_path(r'^.*', include('mock.urls')),
    # path('docs/', schema_view, name='docs'),   # 配置swagger1 docs的url路径

    #swagger2
    # path('swagger(P<format>\.json|\.yaml)', schema_view2.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view2.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view2.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

