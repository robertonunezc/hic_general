# Generated by Django 2.2.6 on 2021-01-25 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210125_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='email',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
