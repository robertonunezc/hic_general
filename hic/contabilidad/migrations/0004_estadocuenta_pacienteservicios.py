# Generated by Django 2.2.6 on 2021-05-11 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_iniciofolio'),
        ('contabilidad', '0003_tabuladorprecios_tipo_cobro'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='estado_cuenta', to='main.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='PacienteServicios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descuento', models.FloatField(default=0.0)),
                ('total', models.FloatField(default=0.0)),
                ('estado_cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contabilidad.EstadoCuenta')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contabilidad.TabuladorPrecios')),
            ],
        ),
    ]
