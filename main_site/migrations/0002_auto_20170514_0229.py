# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-13 19:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalblog',
            name='feeds',
        ),
        migrations.RemoveField(
            model_name='personalblog',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='personalblog',
            name='posts',
        ),
    ]
