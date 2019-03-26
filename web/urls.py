#!/usr/bin/env python
#coding=utf-8


from django.contrib import admin
from django.urls import path,include
from web.views import account
from web.views import customer
from stark.service.stark import site

urlpatterns = [
    path('user/login',account.login),
    path('user/logout',account.logout),
    path('user/code',account.code),
    path('', account.index),
    path('index',account.index),
    path('stark/',site.urls),
]