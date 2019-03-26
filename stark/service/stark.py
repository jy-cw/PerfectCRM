#!/usr/bin/env python
#coding=utf-8

from django.urls import  path
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from stark.utils.Page import Pagination
from django.db.models import Q
import copy
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField,ModelChoiceField


def get_datetime_text(title, field, time_format='%Y-%m-%d'):
    """
    对于Stark组件中定义列时，定制时间格式的数据
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :param time_format: 要格式化的时间格式
    :return:
    """

    def inner(self, obj=None, header=False, *args, **kwargs):
        if header:
            return title
        datetime_value = getattr(obj, field)
        if datetime_value:
            return datetime_value.strftime(time_format)
        else:
            return None

    return inner


class ShowList(object):
    def __init__(self,config,data_list,request):
        self.config = config
        self.data_list = data_list
        self.request = request

        #当前页码
        current_page =int(self.request.GET.get('page',1))
        #数据总数
        data_count = self.data_list.count()
        #请求url路径
        base_url = self.request.path
        self.pagination = Pagination(current_page,data_count,base_url,self.request.GET,page_data_count=10,page_num=5)
        self.page_data = self.data_list[self.pagination.start:self.pagination.end]

        #actions
        self.actions = self.config.new_actions()

    #获取过滤字段
    '''
    数据格式:{
        '所属权限组': [
                "<a href='#' class='active' >全部</a>", '<a href=?group=1 >用户管理</a>', '<a href=?group=2 >权限管理</a>'
                ], 
         '权限': [
                "<a href='#' class='active' >全部</a>", '<a href=?title=%E7%94%A8%E6%88%B7%E5%88%97%E8%A1%A8 >用户列表</a>', '<a href=?title=%E7%BC%96%E8%BE%91%E7%94%A8%E6%88%B7 >编辑用户</a>
                ]
            }
    '''
    def get_filter_linktags(self):
        link_dic = {}
        for filter_field in self.config.list_filter: # ["title","publish","authors",]
            params = copy.deepcopy(self.request.GET)

            #获取当前请求filter的字段值,用来判断是否选中当前过滤字段
            cid=self.request.GET.get(filter_field,0)
            #print("filter_field:",filter_field) # "publish"
            #获取字段对象
            filter_field_obj=self.config.model._meta.get_field(filter_field)

            if isinstance(filter_field_obj,ForeignKey) or isinstance(filter_field_obj,ManyToManyField):
                 # print("filter_field_obj:", filter_field_obj)
                 # print("filter_field_obj.remote_field:", filter_field_obj.remote_field)
                 # print("filter_field_obj.remote_field.model:", filter_field_obj.remote_field.model)
                 # print("filter_field_obj.remote_field.model.objects.all():",filter_field_obj.remote_field.model.objects.all())
                 data_list=filter_field_obj.remote_field.model.objects.all()# 【publish1,publish2...】
            else:
                 data_list=self.config.model.objects.all()

            #print("data_list",data_list)

            temp = []
            if params.get(filter_field):
                del params[filter_field]
                url = params.urlencode()
                link_tag_all = "<a href='?%s' >全部</a>" %url
            else:
                link_tag_all = "<a href='#' class='active' >全部</a>"
            temp.append(mark_safe(link_tag_all))

            for obj in data_list:
                if isinstance(filter_field_obj, ForeignKey) or isinstance(filter_field_obj, ManyToManyField):
                    id = obj.id
                    text =str(obj)
                    params[filter_field] = obj.id
                else:
                    text = getattr(obj,filter_field)
                    params[filter_field] = text
                url=params.urlencode()
                if cid == str(id) or cid == text:
                    link_tag = "<a href=?%s class='active'>%s</a>" % (url,text)
                else:
                    link_tag = "<a href=?%s >%s</a>" % (url, text)
                temp.append(mark_safe(link_tag))

            filter_field_name = filter_field_obj.verbose_name
            link_dic[filter_field_name] = temp

#        print('最终数据:',link_dic)
        return link_dic

    #获取批量操作函数名列表
    # #  [{"func_name":""patch_init,"func_text":"批量初始化"}]
    def get_actions(self):
        actions_list =[]
        for action in self.actions:
            actions_list.append({
                #函数名
                'func_name': action.__name__,
                #中文名
                'func_text': action.text
            })
        return actions_list

   #获取list 页的表头列表
    def get_header(self):
        #构建表头
        header_list = []
        for field in self.config.new_list_display():
            if callable(field):
                header_list.append(field(self.config, header=True))
            elif field == '__str__':
                header_list.append(self.config.model._meta.model_name.upper())
            else:
                header = self.config.model._meta.get_field(field).verbose_name
                header_list.append(header)
        return header_list

   #获取list 页的数据列表
    def get_body(self):
        # 表单数据展示
        new_data_list = []
        for obj in self.page_data:
            temp = []
            for field in self.config.new_list_display():
                #获取字段对象

                # 判断是否是可执行函数
                if callable(field):
                    val = field(self.config, obj)

                else:
                    try:
                        field_obj = self.config.model._meta.get_field(field)
                        # 判断字段是否是多对多字段
                        if field != '__str__' and isinstance(field_obj,ManyToManyField):
                            ret = getattr(obj,field).all()   #<QuerySet [<Role: 开发>, <Role: 运维>]>
                            t = []
                            for i in ret:
                                t.append(str(i))
                            val =','.join(t)

                        else:
                            # 判断字段是否有choices属性
                            if field_obj.choices:
                                fun_val = getattr(obj,'get_' +field + '_display')
                                val = fun_val()
                            # 直接取obj 对应的普通字段数据
                            else:
                                val = getattr(obj, field)
                            # 判断是否在links列表中,如果在则加a标签,多对多字段不加links
                            if field in self.config.list_display_links:
                                change_url = self.config.get_real_url(obj)['change_url']
                                val = mark_safe("<a href='%s'>%s</a>" % (change_url, val))
                    except Exception as  e:
                        val = getattr(obj,field)

                temp.append(val)
            new_data_list.append(temp)
 #           print('new_data_list',new_data_list)
        return new_data_list

class ModelStark(object):
    list_display = ["__str__",]
    list_display_links = []
    modelform_class = None
    search_fields =[]
    actions = []
    list_filter = []

    #默认扩展url
    def extra_url(self):
        return []


    def __init__(self,model,site,prev):
        #self.model 用户当前访问的模型表
        self.model = model
        self.site =site
        self.prev =prev

    #自定义list_display 功能函数
    #编辑,删除操作
    def operation(self,obj=None,header=False):
        if header:
            return '操作'
        change_url = self.get_real_url(obj)['change_url']
        delete_url = self.get_real_url(obj)['delete_url']
        html_code = '<a href="%s" class="btn btn-warning">编辑</a> <a href="%s" class="btn btn-danger">删除</a>' % (change_url,delete_url)
        return mark_safe(html_code)

    #复选框
    def checkbox(self,obj=None,header=False):
        if header:
            return mark_safe('<input id="check_all" type="checkbox">')
        return mark_safe('<input class="qx" type="checkbox" name="selected_id" value=%s>' % obj.id)

    #加入复选框、编辑、删除功能
    #new_list_display = [func,str.....]
    def new_list_display(self):
        temp = []
        temp.append(ModelStark.checkbox)
        temp.extend(self.list_display)
        temp.append(ModelStark.operation)
        return temp

    #加入默认批量删除操作，new_actions=[func,func]
    def new_actions(self):
        temp = []
        temp.append(ModelStark.action_multi_delete)
        temp.extend(self.actions)
        return temp

    #初始化modelform配置
    def get_modelform_class(self, is_add, request, id, *args, **kwargs):
        if not self.modelform_class:
            class ModelFormDemo(ModelForm):
                class Meta:
                    model = self.model
                    fields = '__all__'
            return ModelFormDemo
        else:
            return self.modelform_class

    #初始化批量删除
    def action_multi_delete(self, request,queryset):
        queryset.delete()
        return HttpResponse("批量删除成功")
    action_multi_delete.text = '批量删除'

    #初始化搜索Q对象
    def get_search_q(self,request):
        key_word = request.GET.get('q','')
        self.key_word = key_word
        search_con =Q()
        search_con.connector ='or'
        if key_word:
            for search_field in self.search_fields:
                search_con.children.append((search_field + '__contains',key_word))
        return search_con

    #初始化过滤Q对象
    def get_filter_q(self,request):
        filter_con =Q()
        params = request.GET
        for filter,val in params.items():
            if filter !="page":
                filter_con.children.append((filter,val))
        return filter_con

    #给modelform 里面的外键和多对多字段加入pop功能
    def init_form_pop(self,form):
        for i in form:
            if isinstance(i.field,ModelChoiceField):
                i.is_pop =True
                related_model = i.field.queryset.model
                related_app_label = related_model._meta.app_label
                related_model_name = related_model._meta.model_name
                url = reverse('%s_%s_add'%(related_app_label,related_model_name))
                i.url = url + '?pop_res_id=id_%s' % i.name
        return form

    def save(self, request, form, is_update, *args, **kwargs):
        """
        在使用ModelForm保存数据之前预留的钩子方法
        :param request:
        :param form:
        :param is_update:
        :return:
        """
        return form.save()


    #增删改查视图函数
    def add_view(self, request,*args, **kwargs):
        ModelFormDemo = self.get_modelform_class(True, request, None, *args, **kwargs)
        form_demo = ModelFormDemo()
        form = self.init_form_pop(form_demo)

        if request.method == 'POST':
            form1 = self.init_form_pop(ModelFormDemo(request.POST))
            if form1.is_valid():
                obj = self.save(request,form1,False,*args,**kwargs)
                pop_res_id = request.GET.get('pop_res_id')
                if pop_res_id:
                    res = {'id':obj.id,'text':str(obj),'pop_res_id':pop_res_id}
                    return render(request,'pop.html',{'res':res})
                return redirect(self.get_real_url()['list_url'])
        return render(request,'add.html',locals())

    def change_view(self, request, id, *args, **kwargs):
        ModelFormDemo = self.get_modelform_class(False, request, id, *args, **kwargs)
        edit_obj = self.model.objects.filter(id=id).first()
        form_demo = ModelFormDemo(instance=edit_obj)
        form = self.init_form_pop(form_demo)

        if request.method == 'POST':
            form = self.init_form_pop(ModelFormDemo(request.POST,instance=edit_obj))
            if form.is_valid():
                obj = self.save(request,form,True,*args,**kwargs)
                pop_res_id = request.GET.get('pop_res_id')
                if pop_res_id:
                    res = {'id': obj.id, 'text': str(obj), 'pop_res_id': pop_res_id}
                    return render(request, 'pop.html', {'res': res})
                return redirect(self.get_real_url()['list_url'])
        return render(request,'change.html',locals())

    def delete_view(self, request, id, *args, **kwargs):
        list_url = self.get_real_url()['list_url']
        if request.method == 'POST':
            obj = self.model.objects.filter(id=id).first().delete()
            return redirect(list_url)
        return render(request,'delete.html',locals())

    #用户当前访问的模型表的所有数据
    def get_queryset(self, request, *args, **kwargs):
        return self.model.objects

    def list_view(self, request):
        if request.method =='POST':
            selected_id =request.POST.getlist('selected_id')
            func_name = request.POST.get('action')
            if func_name:
                queryset = self.model.objects.filter(id__in=selected_id)
                func = getattr(self,func_name)
                func(request,queryset)
            else:
                return redirect(self.get_real_url()['list_url'])

        #获取搜索Q对象
        search_q = self.get_search_q(request)

        #获取过滤Q对象
        filter_q = self.get_filter_q(request)

        #经过搜索、过滤之后的所有数据
        data_list =self.get_queryset(request).filter(search_q).filter(filter_q)

        #获取list页面的所有数据
        showlist = ShowList(self,data_list,request)

        #添加url
        add_url =self.get_real_url()['add_url']

        return render(request,'list.html',locals())

    #url的name 名字
    def get_url_name(self):
        app_label, model_name = self.model._meta.app_label, self.model._meta.model_name
        if self.prev:
            return '%s_%s_%s' % (app_label, model_name, self.prev)
        return '%s_%s' % (app_label, model_name)

    #model 实际对应的增删改查url
    def get_real_url(self,obj=None):
        url_dict ={}
        add_url = reverse('%s_add' % self.get_url_name())
        list_url = reverse('%s_list' % self.get_url_name())
        url_dict['add_url'] = add_url
        url_dict['list_url'] = list_url
        if obj:
            change_url = reverse('%s_change' % self.get_url_name(),kwargs={'id':obj.id})
            delete_url = reverse('%s_delete' % self.get_url_name(), kwargs={'id': obj.id})
            url_dict['change_url'] = change_url
            url_dict['delete_url'] = delete_url

        return url_dict


    #分发增删改查url
    def get_urls(self):
        temp =[]
        temp.append(path('',self.list_view,name='%s_list'% self.get_url_name() ))
        temp.append(path('<int:id>/change',self.change_view,name='%s_change'% self.get_url_name()))
        temp.append(path('<int:id>/delete',self.delete_view,name='%s_delete'% self.get_url_name()))
        temp.append(path('add',self.add_view,name='%s_add'% self.get_url_name()))

        #extend 扩展url
        temp.extend(self.extra_url())
        return  temp

    @property
    def urls(self):
        return self.get_urls(),None,None

class StarkSite(object):
    def __init__(self):
        self._registry = []

    def register(self,model,stark_class=None,prev=None):
        if not stark_class:
            stark_class = ModelStark

        # self._registry[model] = stark_class(model,self)
        self._registry.append(
            {'model': model, 'stark_class_obj': stark_class(model,self,prev), 'prev': prev})

    '''
    temp =[
    path('rbac/userinfo/,([path('add',add),path('',list),]None,None),
    path('rbac/role/,([path('add',add),path('',list),]None,None)
    ]
    '''
    def get_urls(self):
        temp = []
#        print('self_reistry:',self._registry)
        for item in self._registry:
            model = item['model']
            stark_class_obj =item['stark_class_obj']
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            if item['prev']:
                temp.append(path('%s/%s/%s/' % (app_label, model_name,item['prev']), stark_class_obj.urls))
            else:
                temp.append(path('%s/%s/' %(app_label,model_name),stark_class_obj.urls))
        return temp

    @property
    def urls(self):
        return self.get_urls(),None,None

site = StarkSite()