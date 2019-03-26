#!/usr/bin/env python
#coding=utf-8

import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from  django.shortcuts import redirect,HttpResponse

class RbacMiddleware(MiddlewareMixin):

    '''
    用户权限校验
    '''

    def process_request(self,request):

        url_record = [
            {'title': '首页', 'url': '/index'}
        ]

        # 当前访问路径
        current_path = request.path_info

        #判断访问路径是否在白名单中
        for valid_url in settings.VALID_URL_LIST:
            # 白名单中的URL无需权限验证即可访问
            if  re.match(valid_url,current_path):
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                request.actions = []
                return None

        # 判断用户是否登录
        if not request.session.get('user_id'):
            return redirect('/user/login')
        else:
            # 需要登录，但无需权限校验
            for url in settings.NO_PERMISSION_LIST:
                if re.match(url,current_path):
                    #默认二级菜单隐藏
                    request.current_selected_permission = 0
                    #设置导航路径为首页
                    request.breadcrumb = url_record
                    return None

        #判断用户是否有对应的权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        flag =False
        for item in permission_dict.values():
            for permission_dict in item['all_permission']:
                permission = '^%s$' % permission_dict['url']
                if re.match(permission,current_path):
                    flag =True

                    request.current_selected_permission = permission_dict['pid'] or permission_dict['id']

                    #追加当前路径到导航路径上
                    #如果没有pid，代表是二级菜单，否则则是二级菜单下的子权限
                    if not permission_dict['pid']:
                        url_record.append({'title':permission_dict['title'],'url':permission_dict['url'],'class': 'active'})
                    else:
                        url_record.append({'title': permission_dict['pid_title'], 'url': permission_dict['pid_url']})
                        url_record.append({'title': permission_dict['title'], 'url': permission_dict['url'],'class': 'active'})
                    request.breadcrumb=url_record

                    #添加权限actions，用来控制按钮粒度
                    request.actions = list(set(item['actions']))
                    break
        if not flag:
            return HttpResponse('抱歉,您没有访问权限')




