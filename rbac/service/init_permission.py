#!/usr/bin/env python
#coding=utf-8

from django.conf import settings

def init_permission(request,current_user):
    """
        用户权限的初始化
        :param current_user: 当前用户对象
        :param request: 请求相关所有数据
        :return:
        """

    # 1.获取当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id','permissions__url','permissions__title','permissions__action','permissions__group_id','permissions__group__title','permissions__pid_id','permissions__pid__title','permissions__pid__url').distinct()
    print(permission_queryset)

    # 2.获取权限中的所有权限url, 只存权限url
    '''
    permission_list=['/user','/user/add']
    '''
    # permission_list = [item['permissions__url'] for item in permission_queryset]

    # 2.把权限url列表、actions操作别名、一级菜单名、二级菜单名存入字典
    '''
    permission_dict = {
        '1': {
            'actions': ['list', 'permission_add', 'permission_edit', 'permission_delete', 'list'], 
            'group_title': '权限管理', 
            'children': [
                    {'id': 1, 'title': '权限列表', 'url': '/stark/rbac/permission/', 'action': 'list', 'pid': None, 'pid_title': None, 'pid_url': None}, 
                    {'id': 5, 'title': '权限组列表', 'url': '/stark/rbac/permissiongroup/', 'action': 'list', 'pid': None, 'pid_title': None, 'pid_url': None}, 
            'all_permission': [
                    {'id': 1, 'title': '权限列表', 'url': '/stark/rbac/permission/', 'action': 'list', 'pid': None, 'pid_title': None, 'pid_url': None}, 
                    {'id': 2, 'title': '添加权限', 'url': '/stark/rbac/permission/add', 'action': 'permission_add', 'pid': 1, 'pid_title': '权限列表', 'pid_url': '/stark/rbac/permission/'},
            }
,
	'2': {
		'actions': ['list', 'customer_add'],
		'group_title': '客户管理',
		'children': [{
			'id': 17,
			'title': '客户列表',
			'url': '/stark/web/customer/',
			'action': 'list',
			'pid': None,
			'pid_title': None,
			'pid_url': None
		}],
		'all_permission': [{
			'id': 17,
			'title': '客户列表',
			'url': '/stark/web/customer/',
			'action': 'list',
			'pid': None,
			'pid_title': None,
			'pid_url': None
		}, {
			'id': 18,
			'title': '添加客户',
			'url': '/stark/web/customer/add',
			'action': 'customer_add',
			'pid': 17,
			'pid_title': '客户列表',
			'pid_url': '/stark/web/customer/'
		}]
	    }
    }
    '''

    permission_dict = {}
    for item in permission_queryset:
        gid = item['permissions__group_id']
        node = {'id': item['permissions__id'], 'title': item['permissions__title'], 'url': item['permissions__url'],
                'action': item['permissions__action'],'pid':item['permissions__pid_id'],'pid_title':item['permissions__pid__title'],'pid_url':item['permissions__pid__url']}
        if not gid in permission_dict:
                permission_dict[gid] ={
                    #用于动态控制按钮粒度
                    'actions':[item['permissions__action']],
                    #权限组名，相当于1级菜单名
                    'group_title': item['permissions__group__title'],
                    # 用于显示二级菜单名
                    'children':[],
                    #用户的所有权限,用于中间件用户权限认证，判断是否有对应的添加、删除、更新、查看权限
                    'all_permission':[node],
                }
        else:
            permission_dict[gid]['actions'].append(item['permissions__action'])
            permission_dict[gid]['all_permission'].append(node)

        # 只有action为list 才需要显示在二级菜单中
        if item['permissions__action'] == 'list':
            permission_dict[gid]['children'].append(node)



    #.存入菜单列表,一级菜单
    # menu_list = []
    # for memu in permission_queryset:
    #     if memu['permissions__action'] == 'list':
    #         menu_list.append((memu['permissions__url'],memu['permissions__group__title']))

    #. 存入菜单字典，二级菜单
    '''
    {
    1: {
        'group_title': '用户管理', 
        'children': [
            {'id': 1, 'title': '用户列表', 'url': '/user'}
            ]
        }, 
    2: {
        'group_title': '角色管理', 
        'children': [
            {'id': 6, 'title': '角色列表', 'url': '/role'}
            ]
        }
    }
    '''
    # menu_dict = {}
    # for memu in permission_queryset:
    #     gid = memu['permissions__group_id']
    #     #只有action为list 才需要显示在菜单中
    #     if memu['permissions__action'] == 'list':
    #         node = {'id': memu['permissions__id'], 'title': memu['permissions__title'], 'url': memu['permissions__url']}
    #         if not gid in menu_dict:
    #             menu_dict[gid] = {
    #                 # 用于显示一级菜单名
    #                 'group_title': memu['permissions__group__title'],
    #                 # 用于显示二级菜单名
    #                 'children': [node,]
    #             }
    #         else:
    #             menu_dict[gid]['children'].append(node)



    #3.把权限dict、菜单dict 存入session中
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    # request.session[settings.MENU_SESSION_KEY] = menu_dict

    print('权限字典',permission_dict)

    request.session['user_id'] = current_user.id