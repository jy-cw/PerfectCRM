#!/usr/bin/env python
#coding=utf-8
from stark.service.stark import site, ModelStark,get_datetime_text
from django.urls import path
from web.models import *
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, redirect, render
from django.db.models import Q
import datetime
from django.http import JsonResponse

class StudyConfig(ModelStark):
    list_display = ["student", "course_record", "record", "score"]

    def patch_late(self, request, queryset):
        queryset.update(record="late")

    patch_late.text = "迟到"
    actions = [patch_late]