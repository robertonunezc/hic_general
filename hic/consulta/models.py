from django.db import models

from hic.main.models import Paciente, Medico
from hic.paciente.models import HistoriaClinica


class TConsulta(models.Model):
    tipo = models.CharField(max_length=80, unique=True)


class Consulta(models.Model):
    fecha = models.DateTimeField()
    tipo = models.ForeignKey(TConsulta, on_delete=models.SET_NULL, null=True)
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.SET_NULL, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)


class NotaPadecimiento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.SET_NULL, null=True)


class TSignoVital(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class SignoVital(models.Model):
    valor = models.FloatField()
    tipo = models.ForeignKey(TSignoVital, on_delete=models.SET_NULL, null=True)


class NotaPadecimientoSignoVital(models.Model):
    nota_padecimiento = models.ForeignKey(NotaPadecimiento, on_delete=models.SET_NULL, null=True)
    signo_vital = models.ForeignKey(SignoVital, on_delete=models.SET_NULL, null=True)


class SConsulta(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)


class SNotaPadecimiento(models.Model):
    s_consulta = models.ForeignKey(SConsulta, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=False)


class SNotaPadecimientoTSignoVital(models.Model):
    s_nota_padecimiento = models.ForeignKey(SNotaPadecimiento, on_delete=models.SET_NULL, null=True)
    t_signo_vital = models.ForeignKey(TSignoVital, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=False)
