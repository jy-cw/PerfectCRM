#!/usr/bin/env python
# -*- coding:utf-8 -*-
from stark.service.stark import ModelStark


class SchoolHandler(ModelStark):
    list_display = ['title']
