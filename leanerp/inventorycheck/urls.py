"""Arya URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from .views import verify_app_login, update_clerk_messages, send_clerk_message, \
                   regenerate_tasks, update_task ,report_inventory, inprogress_inventory, \
                   update_done_task

urlpatterns = [
    # Regular page
    url(r'^update_clerk_messages', update_clerk_messages, name='update_clerk_messages'),
    # API
    url(r'^app_login', verify_app_login, name='app_login'),
    url(r'^send_clerk_message', send_clerk_message, name='send_clerk_message'),
    url(r'^regenerate_tasks', regenerate_tasks, name='regenerate_tasks'),
    url(r'^update_task', update_task, name='update_task'),
    url(r'^report_inventory', report_inventory, name='report_inventory'),
    url(r'^inprogress_inventory', inprogress_inventory, name='inprogress_inventory'),
    url(r'^update_done_task', update_done_task, name='update_done_task'),
]
