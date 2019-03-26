#!/usr/bin/env python
#coding=utf-8

from django import template
from django.conf import settings
from collections import OrderedDict

register = template.Library()

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    '''
    生成一级菜单
    :param request:
    :return:
    '''

    menu_list = request.session.get(settings.MENU_SESSION_KEY)

    return {"menu_list":menu_list}

@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    '''
    生成二级菜单
    :param request:
    :return:
    '''
    multi_menu_dict = request.session.get(settings.PERMISSION_SESSION_KEY)


    #二级菜单默认是展开的
    #return  {'multi_menu_dict':multi_menu_dict}

    #通过设置class，使二级菜单默认不展开

    # 对字典的key进行排序
    key_list = sorted(multi_menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()

    for key in key_list:
        val = multi_menu_dict[key]
        val['class'] = 'hide'

        for per in val['children']:
            if per['id'] == request.current_selected_permission:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val
    return {'multi_menu_dict': ordered_dict}

#导航页
@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'record_list': request.breadcrumb}

#控制按钮粒度,不同用户显示不同按钮
@register.filter
def has_permission(name,request):
    if name in request.actions:
        return True



