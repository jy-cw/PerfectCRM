# Generated by Django 2.1.5 on 2019-03-04 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='roles',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
