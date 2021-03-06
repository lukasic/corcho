# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20160411_0623'),
        ('choosing', '0005_auto_20160412_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolvedCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField()),
                ('choosing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choosing.Choosing')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='resolvedcourse',
            unique_together=set([('choosing', 'course')]),
        ),
    ]
