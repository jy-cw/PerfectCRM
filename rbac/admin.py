from django.contrib import admin
from .models import *

class PerConfig(admin.ModelAdmin):
    list_display = ['title','url','group','action']

# admin.site.register(UserInfo)
admin.site.register(Role)
admin.site.register(Permission,PerConfig)
admin.site.register(PermissionGroup)




