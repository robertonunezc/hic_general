# Generated by Django 2.2.6 on 2020-03-14 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cita', '0006_auto_20200312_1417'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='calenario',
            new_name='calendario',
        ),
    ]
