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

from maintenance_mgmt.views import store_maintenance_mgmt, add_store_maintenance,\
                                   check_recent_maintenance, validate_store_maintenance

urlpatterns = [
	# Page
	url(r'^store_maintenance_mgmt', store_maintenance_mgmt),
    # APIs
    url(r'^add_store_maintenance/', add_store_maintenance),
    url(r'^check_recent_maintenance/', check_recent_maintenance),
    url(r'^validate_store_maintenance/', validate_store_maintenance),
]
