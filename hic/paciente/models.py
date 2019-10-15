from django.db import models

from hic.main.models import Paciente, Medico


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)


class TAlergia(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class AntecedenteAlergia(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.SET_NULL, null=True)
    alergia = models.ForeignKey(TAlergia, on_delete=models.SET_NULL, null=True)