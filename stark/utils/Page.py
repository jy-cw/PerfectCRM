#!/usr/bin/env python
#coding=utf-8

from django.utils.safestring import mark_safe
import copy

class Pagination(object):
    """
    封装分页相关数据
    :param current_page: 当前页码
    :param data_count:    数据库中的数据总条数
    :param base_url: 分页中显示的URL前缀
    :param params: request.GET请求的query值
    :param page_data_count : 每页显示的数据条数
    :param page_num:  最多显示的页码个数
    """

    def __init__(self,current_page,data_count,base_url,params,page_data_count=10,page_num=5):
        self.current_page = current_page
        self.data_count = data_count
        self.page_data_count = page_data_count
        self.page_num = page_num
        self.base_url = base_url

        #request.GET 是不可变的，所以要设置mutable为True
        params = copy.deepcopy(params)
        params._mutable = True
        self.params = params  # self.params : {"page":77,"title":"python","nid":1}

     #起始索引序列
    @property
    def start(self):
        return (self.current_page - 1) * self.page_data_count

    #结束索引序列
    @property
    def end(self):
        return self.current_page * self.page_data_count

    #总的页码数
    @property
    def total_page_num(self):
        num,y = divmod(self.data_count,self.page_data_count)
        if y:
            num +=1
        return  num

    def page_html(self):
        page_list = []
        #处理总页数小于显示的分页数的情况
        if self.total_page_num < self.page_num:
            start_index = 1
            end_index = self.total_page_num + 1
        else:
            #处理出现页码是负数页的情况
            if self.current_page <= (self.page_num +1 )/2:
                start_index = 1
                end_index = self.page_num + 1
            else:
                start_index = self.current_page - (self.page_num - 1)/2
                end_index = self.current_page + (self.page_num + 1)/2
                #处理出现页码大于总页数的情况
                if (self.current_page + (self.page_num - 1 )/2) > self.total_page_num:
                    tart_index = self.total_page_num - self.page_num + 1
                    end_index = self.total_page_num + 1

        #配置首页
        self.params['page']=1
        first_page = '<li><a href="%s?%s">首页</a></li>' % (self.base_url, self.params.urlencode(),)
        page_list.append(first_page)

        #配置上一页
        if self.current_page == 1:
            prev = '<li class="disabled"><a  href="javascript:void(0);">上一页</a></li>'
        else:
            self.params["page"] = self.current_page - 1
            prev = '<li><a  href="%s?%s">上一页</a></li>' % (self.base_url, self.params.urlencode(),)
        page_list.append(prev)

        #配置页码页
        for i in range(int(start_index),int(end_index)):
            self.params["page"] = i
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?%s">%s</a></li>' % (self.base_url, self.params.urlencode(), i)
            else:
                temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.params.urlencode(), i)
            page_list.append(temp)


        #配置下一页
        if self.current_page == self.total_page_num:
            nex = '<li class="disabled"><a  href="javascript:void(0);">下一页</a></li>'
        else:
            self.params['page'] = self.current_page + 1
            nex = '<li><a href="%s?%s">下一页</a></li>' % (self.base_url, self.params.urlencode(),)

        page_list.append(nex)

        #配置尾页
        self.params["page"] = self.total_page_num
        last_page = '<li><a href="%s?%s">尾页</a></li>' % (self.base_url, self.params.urlencode(),)
        page_list.append(last_page)


        #配置跳转页
        jump = """   
       &#12288<label class="form-inline"><input id="jumppage" type="text" style="width:50px" class="form-control  "></label> <button type="submit" class="btn btn-info " onclick='jumpTo(this, "%s?page=");'>跳转到</button>
                            <script>
                                function jumpTo(ths,base){
                                    var val = document.getElementById("jumppage").value;
                                    location.href = base + val;
                                }
                            </script>
                            """ % (self.base_url,)

        page_list.append(jump)

        page_str = mark_safe("".join(page_list))

        return page_str

