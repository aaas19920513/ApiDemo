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
from django.urls import path, include
from rest_framework import routers
from users import views
from rest_framework_jwt.views import obtain_jwt_token
from runner import views as runner_views

# 删除尾部斜杠 trailing_slash=False
router = routers.DefaultRouter()
# router.register(r'register', views.RegisterViewSet, base_name='register')
# router.register(r'test', views.BatchLoadView, base_name='test')

# router.register('project', runner_views.ProjectView, base_name='project')
router.register('module', runner_views.ModuleView, base_name='module')
router.register('case', runner_views.CaseView, base_name='case')
router.register('step', runner_views.StepView, base_name='step')

urlpatterns = [

    path('api/', include('users.urls')),
    path('api/', include('runner.urls')),
    path('admin/', admin.site.urls),
    #jwt的token认证
    # path('login/', obtain_jwt_token),
    path('', include(router.urls)),
]
