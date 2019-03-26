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

class ConsultConfig(ModelStark):
    list_display = ["customer", "consultant", get_datetime_text('跟进时间',"date"), "note"]