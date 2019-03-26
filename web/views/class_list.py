#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django.urls import reverse
from stark.service.stark import ModelStark
from stark.forms.widgets import DateTimePickerInput
from web import models
from django.forms import ModelForm
from  stark.service.stark import get_datetime_text


class ClassListModelForm(ModelForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'
        widgets = {
            'start_date': DateTimePickerInput,
            'graduate_date': DateTimePickerInput,
        }


class ClassListHandler(ModelStark):

    def display_course(self, obj=None, header=None, *args, **kwargs):
        if header:
            return '班级'
        return str(obj)

    def display_course_record(self, obj=None, header=None, *args, **kwargs):
        if header:
            return '上课记录'
        record_url = '#'
        return mark_safe('<a target="_blank" href="%s">上课记录</a>' % record_url)

    list_display = [
        'school',
        display_course,
        'price',
        get_datetime_text('开班日期','start_date'),
        'tutor',
        'teachers',
        display_course_record
    ]

    modelform_class = ClassListModelForm

