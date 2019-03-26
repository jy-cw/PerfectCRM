#!/usr/bin/env python
#coding=utf-8

from django.forms import ModelForm
from stark.forms.widgets import DateTimePickerInput
from web import models
from django.urls import reverse,path
from django.shortcuts import HttpResponse, redirect, render
from django.db.models import Q
from stark.service.stark import ModelStark,get_datetime_text
import datetime

class All_Cusotmer(ModelStark):
    class CusotmerModelForm(ModelForm):
        class Meta:
            model = models.Customer
            fields = '__all__'
            widgets = {
                'date': DateTimePickerInput,
                'recv_date': DateTimePickerInput,
                'last_consult_date': DateTimePickerInput,
            }


    list_display = ["name", 'gender', 'course', "consultant",get_datetime_text('当前销售的接单日期','recv_date'),get_datetime_text('最后跟进日期','last_consult_date') ]
    modelform_class = CusotmerModelForm


    # def public_customer(self, request):
    #     # 未报名 且3天未跟进或者15天未成单
    #     now = datetime.datetime.now()
    #
    #     # 三天未跟进 now-last_consult_date>3   --->last_consult_date<now-3
    #     # 15天未成单 now-recv_date>15   --->recv_date<now-15
    #
    #     delta_day3 = datetime.timedelta(days=3)
    #     delta_day15 = datetime.timedelta(days=15)
    #     user_id = request.session.get("user_id")
    #     customer_list = models.Customer.objects.filter(
    #         Q(last_consult_date__lt=now - delta_day3) | Q(recv_date__lt=now - delta_day15), status=2).exclude(consultant=user_id)
    #     print(customer_list)
    #     return render(request, "public.html", locals())
    #
    # def further(self, request, customer_id):
    #
    #     user_id = request.session.get("user_id")
    #
    #     now = datetime.datetime.now()
    #     delta_day3 = datetime.timedelta(days=3)
    #     delta_day15 = datetime.timedelta(days=15)
    #
    #
    #     # 为改客户更改课程顾问，和对应时间
    #     ret = models.Customer.objects.filter(pk=customer_id).filter(
    #         Q(last_consult_date__lt=now - delta_day3) | Q(recv_date__lt=now - delta_day15), status=2).update(
    #         consultant=user_id, last_consult_date=now, recv_date=now)
    #     if not ret:
    #         return HttpResponse("已经被跟进了")
    #
    #     models.CustomerDistrbute.objects.create(customer_id=customer_id, consultant_id=user_id, date=now, status=1)
    #
    #     return HttpResponse("跟进成功")
    #
    #
    # def extra_url(self):
    #
    #     temp = []
    #     temp.append(path("public/", self.public_customer))
    #     temp.append(path("further/<int:customer_id>", self.further))
    #
    #     return temp