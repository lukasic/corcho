# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 04:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20160411_0623'),
        ('accounts', '0003_auto_20160411_0623'),
        ('choosing', '0003_auto_20160331_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeniedCombination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='choose',
            options={'verbose_name': 'Študentov zápis', 'verbose_name_plural': 'Zápisy študentov'},
        ),
        migrations.AlterModelOptions(
            name='choosing',
            options={'ordering': ('priority',), 'verbose_name': 'Nastavenia pre zápis', 'verbose_name_plural': 'Nastavenia pre zápisy'},
        ),
        migrations.AlterModelOptions(
            name='teacherrequest',
            options={'verbose_name': 'Žiadosť o učiteľa', 'verbose_name_plural': 'Žiadosti o učiteľov'},
        ),
        migrations.AlterField(
            model_name='choose',
            name='phase',
            field=models.IntegerField(choices=[(0, 'Čaká sa'), (1, 'Schválené'), (2, 'Odmietnuté'), (3, 'Zmazané')], default=0),
        ),
        migrations.AlterField(
            model_name='choosing',
            name='phase',
            field=models.IntegerField(choices=[(0, 'Príprava'), (1, 'Zápis predmetov/seminárov'), (2, 'Vyhodnotenie možností'), (3, 'Zmeny v zápisoch'), (4, 'Vytváranie skupín'), (5, 'Zmeny v skupinách'), (6, 'Ukončené')]),
        ),
        migrations.AlterField(
            model_name='teacherrequest',
            name='phase',
            field=models.IntegerField(choices=[(0, 'Čaká sa'), (1, 'Schválené'), (2, 'Odmietnuté')], default=0),
        ),
        migrations.AddField(
            model_name='deniedcombination',
            name='choosing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choosing.Choosing'),
        ),
        migrations.AddField(
            model_name='deniedcombination',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='deniedcombination',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Teacher'),
        ),
    ]
