# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-02 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_citas_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citas',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
