# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 17:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ('grade', 'name')},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('classroom', 'user'), 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
    ]
