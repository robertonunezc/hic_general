from django.db import models

from hic.main.models import Medico, Paciente, EspecialidadMedico


class Calendario(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)


class TFrecuenciaRepeticion(models.Model):
    NO_REPETIR = 0
    DIARIA = 1
    SEMANAL = 2
    MENSUAL = 3
    ANUAL = 4

    FRECUENCIA = (
        (NO_REPETIR, "NO REPETIR"),
        (DIARIA, "TODOS LOS DIAS"),
        (SEMANAL, "SEMANALMENTE"),
        (MENSUAL, "MENSUALMENTE"),
        (ANUAL, "ANUALMENTE")
    )

    frecuencia = models.IntegerField(choices=FRECUENCIA, unique=True)


class SlotBloqueado(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    frecuencia = models.ForeignKey(TFrecuenciaRepeticion, on_delete=models.SET_NULL, null=True)
    calendario = models.ForeignKey(Calendario, on_delete=models.CASCADE)


class ECita(models.Model):
    CANCELADA = -1
    RESERVADA = 0
    CONFIRMADA = 1
    TERMINADA = 2

    ESTADO = (
        (CANCELADA, "CANCELADA"),
        (RESERVADA, "RESERVADA"),
        (CONFIRMADA, "CONFIRMADA"),
        (TERMINADA, "TERMINADA")
    )

    estado = models.IntegerField(choices=ESTADO, unique=True)


class TCita(models.Model):
    INICIAL = 1
    SEGUIMIENTO = 2

    TIPO = (
        (INICIAL, "INICIAL"),
        (SEGUIMIENTO, "SEGUIMIENTO"),
    )

    tipo = models.IntegerField(choices=TIPO, unique=True)


class Cita(models.Model):
    fecha = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    medico_especialidad = models.ForeignKey(EspecialidadMedico, on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey(ECita, on_delete=models.SET_NULL, null=True)
    tipo = models.ForeignKey(TCita, on_delete=models.SET_NULL, null=True)
    calendario = models.ForeignKey(Calendario, on_delete=models.SET_NULL, null=True)
