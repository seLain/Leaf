"""leanerp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from leanerp import settings

from .views import index, logout

import notifications.urls # refers to django-notifications-hq module

urlpatterns = [
    # Regular pages
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^logout/', logout),
    url(r'^erpadmin/', include('erpadmin.urls')),
    url(r'^maintenance_mgmt/', include('maintenance_mgmt.urls')),
    # APIs
    url(r'^inventorycheck/', include('inventorycheck.urls')),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^api_v1/', include('api_v1.urls')),
    # serving media files
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
