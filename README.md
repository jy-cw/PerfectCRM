## CRM

[![Python3](https://img.shields.io/badge/python-3.7-green.svg?style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-2.1-brightgreen.svg?style=plastic)](https://www.djangoproject.com/)

----

### 功能

CRM，客户关系管理系统（Customer Relationship Management）。企业用CRM技术来管理与客户之间的关系，以求提升企业成功的管理方式，其目的是协助企业管理销售循环：新客户的招徕、保留旧客户、提供客户服务及进一步提升企业和客户的关系，并运用市场营销工具，提供创新式的个人化的客户商谈和服务，辅以相应的信息系统或信息技术如数据挖掘和数据库营销来协调所有公司与顾客间在销售、营销以及服务上的交互。

此系统主要是以教育行业为背景，为公司开发的一套客户关系管理系统。系统分为三部分：
1. 权限系统，一个独立的rbac组件；
2. stark组件，一个独立的curd组件；
3. crm业务，以教育行业为背景并整合以上两个组件开发一套系统。


### 开始使用

克隆`PerfectCRM`仓库到本地, 然后进入仓库目录，执行以下命令

```
# cd /path/PerfectCRM
# pip install -r requiremenets/requirements.txt
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver IP:Port 
```

### 测试Demo

```
访问地址:http://IP:8000/
用户名: cw
密码: 123
```


### 数据库配置
数据库默认使用SQLite3, 如果使用其他数据库请修改`/PATH/PerfectCRM/PerfectCRM/settings.py` 文件
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名',
        'USER': '数据库账号',
        'PASSWORD': '数据库密码',
        'HOST': '数据库地址',
        'PORT': '3306',
    }
}
```

