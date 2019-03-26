#!/usr/bin/env python
#coding=utf-8

from django.shortcuts import render,HttpResponse,redirect
from rbac.models import *
from web.models import *
from rbac.service.init_permission import init_permission
from web.utils import code_en,code_cn

def code(request):
    buf_str,code = code_en.generate_verification_code()
    #buf_str,code = code_cn.generate_verification_cn_code()
    request.session['code'] = code
    return HttpResponse(buf_str)



def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        if request.POST.get('code').lower() == request.session.get('code').lower():
            user = request.POST.get('username')
            password = request.POST.get('password')

            current_user = UserInfo.objects.filter(name=user,password=password).first()
            if not current_user:
                return render(request,'login.html',{'msg':'用户名或密码错误'})

            init_permission(request,current_user)
            return redirect('/index')
        else:
            err_msg = '验证码错误'
            return render(request, 'login.html', {'msg': err_msg})




def logout(request):
    request.session.delete()
    return redirect('/user/login')

def index(request):
    current_user_id = request.session.get('user_id')
    current_user = UserInfo.objects.filter(id=current_user_id).first()
    return render(request,'index.html',locals())

