#!/usr/bin/env python
#coding=utf-8

from  django.shortcuts import redirect,render,HttpResponse
from rbac.models import *
from web.models import *


def user(request):
    current_user_id = request.session.get('user_id')
    current_user = UserInfo.objects.filter(id=current_user_id).first()
    user_list = UserInfo.objects.all()
    return render(request,'rbac/users.html',locals())

def user_add(request):
    return HttpResponse('添加用户')

def user_edit(request,uid):
    return HttpResponse('修改用户:%s' %uid)

def user_del(request,uid):
    return  HttpResponse('删除用户:%s' %uid)



def role(request):
    current_user_id = request.session.get('user_id')
    current_user = UserInfo.objects.filter(id=current_user_id).first()
    role_list = Role.objects.all()
    return render(request,'rbac/roles.html',locals())

def role_add(request):
    return HttpResponse('添加角色')

def role_edit(request,uid):
    return HttpResponse('修改角色:%s' %uid)

def role_del(request,uid):
    return  HttpResponse('删除角色:%s' %uid)

def role(request):
    current_user_id = request.session.get('user_id')
    current_user = UserInfo.objects.filter(id=current_user_id).first()
    role_list = Role.objects.all()
    return render(request,'rbac/roles.html',locals())

def permission_add(request):
    UserInfo.objects.bulk_create()
    return HttpResponse('添加权限')

def permission_edit(request,uid):
    return HttpResponse('修改权限:%s' %uid)

def permission_del(request,uid):
    return  HttpResponse('删除权限:%s' %uid)

def permission(request):
    current_user_id = request.session.get('user_id')
    current_user = UserInfo.objects.filter(id=current_user_id).first()
    permission_list = Permission.objects.all()
    # for permission in permission_list:
    #     print('getattr:',getattr(permission,'group'))
    return render(request,'rbac/permission.html',locals())