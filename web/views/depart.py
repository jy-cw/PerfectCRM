#!/usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service.stark import ModelStark


class DepartmentHandler(ModelStark):
    list_display = ['title', ]
