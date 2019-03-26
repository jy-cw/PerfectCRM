#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.urls import path,reverse
from web.models import *
from django.shortcuts import HttpResponse, render, redirect
from stark.service.stark import ModelStark
from django.forms import ModelForm

class UserInfoAddModelForm(ModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']
        widgets = {
            'password':forms.PasswordInput,
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = password
        return self.cleaned_data

class UserInfoChangeModelForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = password
        return self.cleaned_data


class UserInfoHandler(ModelStark):

    # 自定义多对多展示
    def roles_display(self, obj=None, header=False):
        if header:
            return '角色列表'
        temp = []
        for role in obj.roles.all():
            s = "<a href='%scancel_role/%s/%s' style='border:1px solid #369;padding:3px 6px'><span>%s</span></a>&nbsp;" % (
                self.get_real_url()['list_url'], obj.id, role.id, role.title,)
            temp.append(s)
        return mark_safe("".join(temp))

    def display_reset_pwd(self, obj=None, header=None, *args, **kwargs):
        if header:
            return '重置密码'
        reset_url = reverse('reset_pwd',kwargs={'id':obj.id})
        return mark_safe("<a href='%s'>重置密码</a>" % reset_url)

    list_display = ['nickname', 'gender', 'phone', 'email', 'depart', roles_display,display_reset_pwd]


    #覆盖父类的get_modelform_class 方法，可以针对统计 编辑 显示不同的form表单字段
    def get_modelform_class(self, is_add, request, pk, *args, **kwargs):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    search_fields = ['nickname', 'name']
    list_filter = ['roles', 'depart']


    def reset_password(self, request, id):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = UserInfo.objects.filter(id=id).first()
        rest_user = userinfo_object.nickname
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'change.html', {'form': form,'rest_user':rest_user})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save()
            return redirect(self.get_real_url()['list_url'])

        return render(request, 'change.html', {'form': form,'rest_user':rest_user})


    def cancel_role(self, *args, **kwargs):
        user_obj = UserInfo.objects.filter(id=kwargs['uid']).first()
        user_obj.roles.remove(kwargs['rid'])
        return redirect(self.get_real_url()['list_url'])


    # 自定义扩展url
    def extra_url(self):
        temp = []
        temp.append(path("reset/password/<int:id>/", self.reset_password,name='reset_pwd'))
        temp.append(path("cancel_role/<int:uid>/<int:rid>", self.cancel_role))
        return temp
