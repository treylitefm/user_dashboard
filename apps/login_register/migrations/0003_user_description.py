# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0002_user_user_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(default='', max_length=512),
        ),
    ]