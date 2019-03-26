#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe
from django.urls import reverse,path
from stark.service.stark import ModelStark,get_datetime_text
from django.forms import ModelForm
from web import models
from django.shortcuts import HttpResponse, redirect, render
from django.db import transaction
from stark.forms.widgets import DateTimePickerInput

class PublicCustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', ]
        widgets = {
            'date': DateTimePickerInput,
            'recv_date': DateTimePickerInput,
            'last_consult_date': DateTimePickerInput,
        }


class PublicCustomerHandler(ModelStark):

    def display_record(self, obj=None, header=None, *args, **kwargs):
        if header:
            return '跟进记录'
        record_url = '/stark/web/consultrecord/?customer=%s' % obj.id
        return mark_safe('<a href="%s">查看跟进记录</a>' % record_url)

    list_display = ["name", 'gender', 'course', 'status',get_datetime_text('接单日期', 'recv_date'),get_datetime_text('最后跟进日期', 'last_consult_date'), display_record]

    modelform_class = PublicCustomerModelForm

    def get_queryset(self, request, *args, **kwargs):
        return self.model.objects.filter(consultant__isnull=True)

    def extra_url(self):
        temp=[]
        temp.append(path('record/<int:id>/$', self.record_view))
        return temp

    def record_view(self, request, id):
        """
        查看跟进记录的视图
        :param request:
        :param pk:
        :return:
        """
        record_list = models.ConsultRecord.objects.filter(customer_id=id)
        return render(request, 'record_view.html', {'record_list': record_list})

    def action_multi_apply(self, request, *args, **kwargs):
        """
        批量申请到私户
        :return:
        """
        current_user_id = request.session.get("user_id")
        id_list = request.POST.getlist('selected_id')

        private_customer_count = models.Customer.objects.filter(consultant_id=current_user_id, status=2).count()

        # 私户个数限制
        if (private_customer_count + len(id_list)) > models.Customer.MAX_PRIVATE_CUSTOMER_COUNT:
            return HttpResponse('做人不要太贪心，私户中已有%s个客户，最多只能申请%s' % (
                private_customer_count, models.Customer.MAX_PRIVATE_CUSTOMER_COUNT - private_customer_count))

        # 数据库中加锁
        flag = False
        with transaction.atomic():  # 事务
            # 在数据库中加锁
            origin_queryset = models.Customer.objects.filter(id__in=id_list, status=2,
                                                             consultant__isnull=True).select_for_update()
            if len(origin_queryset) == len(id_list):
                models.Customer.objects.filter(id__in=id_list, status=2,
                                               consultant__isnull=True).update(consultant_id=current_user_id)
                flag = True

        if not flag:
            return HttpResponse('手速太慢了，选中的客户已被其他人申请，请重新选择')

    action_multi_apply.text = "申请到我的私户"

    actions = [action_multi_apply, ]
