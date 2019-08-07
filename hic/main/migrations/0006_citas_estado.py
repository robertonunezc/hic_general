# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-02 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20181201_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='citas',
            name='estado',
            field=models.IntegerField(choices=[(0, 'Agendada'), (1, 'Confirmada'), (2, 'Cancelada')], default=0),
        ),
    ]
