#!/usr/bin/env python
#coding=utf-8
from stark.service.stark import site,ModelStark
from rbac.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from django.shortcuts import HttpResponse,render,redirect
from django.urls import path


#自定义modelForm
class BookModelForm(ModelForm):
    class Meta:
        model = Permission
        fields = "__all__"

        labels={
            "title":"书籍名称",
            "price":"价格"
        }


class PermissionConfig(ModelStark):
    list_display = ['id','title','url','action','group','pid']
    list_display_links = ['id']
    # modelform_class = BookModelForm
    search_fields = ['title','action']

    #批量操作
    def patch_init(self, request, queryset):
        print(queryset)
        # queryset.update(price=123)

        return HttpResponse("批量打印OK")

    patch_init.text = "批量打印"
    actions = [patch_init]
    # 过滤
    list_filter = ['group',]
site.register(Permission,PermissionConfig)

site.register(Role)
site.register(PermissionGroup)