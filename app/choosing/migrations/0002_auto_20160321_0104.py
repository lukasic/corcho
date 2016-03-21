# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choosing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choose',
            name='phase',
            field=models.IntegerField(choices=[(0, 'Waiting'), (1, 'Approved'), (2, 'Denied'), (3, 'Deleted')], default=0),
        ),
    ]
