#!/usr/bin/env python
# coding=utf-8
from django.utils.module_loading import import_string
from django.conf import settings
from rbac import models
from django.shortcuts import render, redirect, HttpResponse

def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """

    user_id = request.GET.get('uid')
    # 业务中的用户表
    user_model_class = import_string(settings.RBAC_USER_MODLE_CLASS)

    user_object = user_model_class.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    # 用户分配角色
    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')
        user_object.roles.set(role_id_list)

    #角色分配权限
    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色，然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}

    # 获取当前用户用户用户的所有权限

    # 如果选中的角色，优先显示选中角色所拥有的权限
    # 如果没有选择角色，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        #获取角色拥有的所有权限
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
        #{1: None, 2: None, 3: None}

    elif user_object:  # 未选择角色，但选择了用户
        #获取用户的角色的所有权限
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id','permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    all_user_list = user_model_class.objects.all()

    all_role_list = models.Role.objects.all()


    # 所有的菜单（一级菜单,也就是所有的权限组名）
    all_menu_list = models.PermissionGroup.objects.values('id', 'title')
    """
    <QuerySet [{'id': 1, 'title': '权限管理'}, {'id': 2, 'title': '客户管理'}, {'id': 3, 'title': '校区管理'}, {'id': 4, 'title': '学员管理'}]>]
    """

    all_menu_dict = {}
    """
       {
           一级菜单ID:{id:1,title:一级菜单名,children:[]},
           一级菜单ID:{id:2,title:一级菜单名,children:[]},
       }
       """
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item



    # 所有二级菜单,action为list的权限
    all_second_menu_list = models.Permission.objects.filter(action='list').values('id', 'title', 'group_id')
    """
    <QuerySet [{'id': 1, 'title': '权限列表', 'group_id': 1}, {'id': 5, 'title': '权限组列表', 'group_id': 1}, {'id': 9, 'title': '角色列表', 'group_id': 1}]
    """
    all_second_menu_dict = {}
    """
        {
            二级菜单ID:{id:二级菜单ID,title:二级菜单名, group_id:关联的一级菜单ID,children:[] },   
            二级菜单ID:{id:二级菜单ID,title:二级菜单名, group_id:关联的一级菜单ID,children:[] }, 
        }
        """
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row

        group_id = row['group_id']
        all_menu_dict[group_id]['children'].append(row)



    # 所有三级菜单（不能做菜单的权限,action不是list）
    all_permission_list = models.Permission.objects.exclude(action='list').values('id', 'title', 'pid_id')
    """
    <QuerySet [{'id': 2, 'title': '添加权限', 'pid_id': 1}, {'id': 3, 'title': '编辑权限', 'pid_id': 1}, {'id': 4, 'title': '删除权限', 'pid_id': 1}]
    """

    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)


    """
    最终querySet数据结构:
      [
           {
           一级菜单ID:{id:1,title:一级菜单名,children:[{id:1,title:二级菜单1, group_id:1,children:[{id:11,title:菜单下的所有权限,pid:1},]},{id:3,title:二级菜单2, group_id:3,children:[] },]},
           一级菜单ID:{id:2,title:一级菜单名,children:[{id:2,title:二级菜单1, group_id:2,children:[{id:11,title:菜单下的所有权限,pid:2},]},{id:4,title:二级菜单2, group_id:4,children:[] },]},
       }
    ]
    示例:

    [
        {
            'id': 1,
            'title': '权限管理',
            'children': [
                    {'id': 1,'title': '权限列表','group_id': 1,'children': [{'id': 2,'title': '添加权限','pid_id': 1}, {'id': 3,'title': '编辑权限','pid_id': 1},]}, 
                    {'id': 5,'title': '权限组列表','group_id': 1,'children': [{'id': 6,'title': '编辑权限组','pid_id': 5}, {'id': 7,'title': '删除权限组','pid_id': 5},
               ]
        },
        {
            'id': 2,
            'title': '客户管理',
            'children': [
                    {'id': 17,'title': '客户列表','group_id': 2,'children': [{'id': 18,'title': '添加客户','pid_id': 17}, {'id': 39,'title': '编辑客户','pid_id': 17},]}, 
                    {'id': 36,'title': '公户列表','group_id': 2,'children': [{'id': 41,'title': '确认跟进','pid_id': 36}, {'id': 42,'title': '添加公户','pid_id': 36},]},
              ]
        },
     ]
    """
    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
        }
    )
