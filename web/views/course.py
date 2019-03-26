#!/usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service.stark import ModelStark

class CourseHandler(ModelStark):
    list_display = ['name', ]
