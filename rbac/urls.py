#!/usr/bin/env python
#coding=utf-8
from django.urls import path
from rbac import views

urlpatterns = [
    path('distribute/permissions/', views.distribute_permissions, name='rbac_permission_list'),
]