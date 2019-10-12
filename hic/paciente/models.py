from django.db import models

from hic.main.models import Paciente, Medico


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)


class Antecedente(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.SET_NULL, null=True)


class TAlergia(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class Alergia(models.Model):
    edad_comienzo = models.IntegerField()
    tipo = models.ForeignKey(TAlergia, on_delete=models.SET_NULL, null=True)


class AntecedenteAlergia(models.Model):
    antecedente = models.ForeignKey(Antecedente, on_delete=models.SET_NULL, null=True)
    alergia = models.ForeignKey(Alergia, on_delete=models.SET_NULL, null=True)


class SAntecedente(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)


class SAntecedenteTAlergia(models.Model):
    s_antecedente = models.ForeignKey(SAntecedente, on_delete=models.SET_NULL, null=True)
    t_alergia = models.ForeignKey(TAlergia, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=False)