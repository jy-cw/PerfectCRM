from django.db import models



class PermissionGroup(models.Model):
    '''
    权限组表.可以做为菜单名显示
    '''
    title = models.CharField(verbose_name='权限组名', max_length=32)

    def __str__(self):
        return self.title

class Permission(models.Model):
    '''
    权限表
    '''
    title = models.CharField(verbose_name='权限',max_length=32)
    url = models.CharField(verbose_name='权限URL',max_length=128)
    action = models.CharField(verbose_name='动作',max_length=32, default="")
    group = models.ForeignKey(verbose_name='所属权限组',to='PermissionGroup',default=1,on_delete=models.CASCADE)
    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission', null=True, blank=True, related_name='parents',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单',on_delete=models.CASCADE,limit_choices_to={'action':'list'})

    def __str__(self):
        return self.title

class Role(models.Model):
    '''
    角色表
    '''
    title = models.CharField(verbose_name='角色',max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限',to='Permission',blank=True)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    email = models.EmailField(verbose_name='邮箱',max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色',to=Role,blank=True)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    def __str__(self):
        return self.name

    class Meta:
        # django以后再做数据库迁移时，不再为UserInfo类创建相关的表以及表结构了。
        # 此类可以当做"父类"，被其他Model类继承。
        abstract = True
