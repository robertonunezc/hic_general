# Generated by Django 2.2.6 on 2019-10-28 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191024_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='NCodigoPostal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=80, unique=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NColonia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('activo', models.BooleanField(default=True)),
                ('codigo_postal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.NCodigoPostal')),
            ],
        ),
        migrations.RenameModel(
            old_name='TEstado',
            new_name='NEstado',
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='municipio',
        ),
        migrations.AddField(
            model_name='nmunicipio',
            name='estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.NEstado'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='direccion',
            name='codigo_postal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.NColonia'),
        ),
        migrations.AlterField(
            model_name='nmunicipio',
            name='nombre',
            field=models.CharField(max_length=80),
        ),
        migrations.AddField(
            model_name='ncodigopostal',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.NMunicipio'),
        ),
    ]
