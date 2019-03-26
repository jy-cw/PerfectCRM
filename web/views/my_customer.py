#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django.urls import reverse,path
from stark.service.stark import ModelStark,get_datetime_text
from django.forms import ModelForm
from web import models
from stark.forms.widgets import DateTimePickerInput



class MyCustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', ]
        widgets = {
            'date': DateTimePickerInput,
            'recv_date': DateTimePickerInput,
            'last_consult_date': DateTimePickerInput,
        }


class MyCustomerHandler(ModelStark):
    modelform_class  = MyCustomerModelForm

    def display_record(self, obj=None, header=None, *args, **kwargs):
        if header:
            return '跟进'
        record_url = '/stark/web/consultrecord/?customer=%s' % obj.id
        return mark_safe('<a target="_blank" href="%s">跟进</a>' % record_url)


    list_display = ["name", 'gender', 'course', 'status',get_datetime_text('接单日期','recv_date'),get_datetime_text('最后跟进日期','last_consult_date') ,display_record]


    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session.get("user_id",None)
        return self.model.objects.filter(consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            current_user_id = request.session.get("user_id")
            form.instance.consultant_id = current_user_id
        form.save()

    def action_multi_remove(self, request, *args, **kwargs):
        """
        批量移除到公户
        :return:
        """
        current_user_id = request.session.get("user_id")
        id_list = request.POST.getlist('selected_id')
        models.Customer.objects.filter(id__in=id_list, consultant_id=current_user_id).update(consultant=None)

    action_multi_remove.text = "移除到公户"

    actions = [action_multi_remove]

