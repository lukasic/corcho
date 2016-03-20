# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20160320_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('acronym', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('info_goal', models.CharField(blank=True, default='', max_length=512)),
                ('info_content', models.CharField(blank=True, default='', max_length=512)),
                ('info_anotations', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name': 'Course',
                'ordering': ('-active', 'acronym'),
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name': 'Course category',
                'verbose_name_plural': 'Course categories',
            },
        ),
        migrations.CreateModel(
            name='SubjectClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acronym', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('teachers', models.ManyToManyField(blank=True, null=True, related_name='subject_class', to='accounts.Teacher')),
            ],
            options={
                'verbose_name': 'Subject class',
                'verbose_name_plural': 'Subject classes',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.CourseCategory'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.SubjectClass'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, to='accounts.Teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('name', 'category')]),
        ),
    ]
