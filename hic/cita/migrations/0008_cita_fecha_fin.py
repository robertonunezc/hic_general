# Generated by Django 2.2.6 on 2021-02-18 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cita', '0007_auto_20210106_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='fecha_fin',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]