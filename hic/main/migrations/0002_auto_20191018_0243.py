# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-18 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='telefono',
            field=models.CharField(max_length=16),
        ),
    ]