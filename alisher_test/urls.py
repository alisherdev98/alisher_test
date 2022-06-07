"""alisher_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from employee.views import *
from .yasg import urlpatterns as urlpattern_yasg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/employee/', CreateEmployeeAPIView.as_view(), name='employee_create'),
    path('api/v1/employee/<int:pk>/', OneEmployeeAPIView.as_view(), name='employee_retrieve'),
    path('api/v1/changestatus/', UpdateStatusAPIView.as_view()),
    path('api/v1/changeleader/', ChangeLeaderAPIView.as_view()),
    path('api/v1/login/', LoginAPIView.as_view()),
    path(r'api-auth', include('rest_framework.urls'), name='rest_framework')
]

urlpatterns += urlpattern_yasg
