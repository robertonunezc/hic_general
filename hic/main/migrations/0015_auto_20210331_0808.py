# Generated by Django 2.2.6 on 2021-03-31 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210218_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='estado',
            field=models.CharField(default='ACTIVO', help_text='BAJA, ACTIVO', max_length=500),
        ),
    ]