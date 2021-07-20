"""Deals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from files.views import FilesViewSet
from topcustomers.views import TopCustomersViewSet

router = DefaultRouter()
router.register(r'files', FilesViewSet)
#router.register(r'topcustomers', TopCustomersViewSet)

urlpatterns = [
    path(r'topcustomers/<file_name>', TopCustomersViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
