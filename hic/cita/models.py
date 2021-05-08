from django.db import models

from hic.main.models import Medico, Paciente
import json
from colorfield.fields import ColorField


class Calendario(models.Model):
    nombre = models.CharField(max_length=200, default="Clínica General")
    medico = models.ForeignKey(
        Medico, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre.__str__()


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

    def __str__(self):
        for item in self.ESTADO:
            if item[0] == self.estado:
                return item[1]
        return self.estado


class TCita(models.Model):

    tipo = models.CharField(default="", max_length=50)
    color = ColorField(max_length=20, default="#3788d8")

    class Meta:
        verbose_name = "Tipo Cita"

    def __str__(self):
        return self.tipo


class Cita(models.Model):
    titulo = models.CharField(max_length=100, default="Horario de Consulta")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name='citas', null=True, blank=True)
    medico = models.ForeignKey(
        Medico, on_delete=models.PROTECT, related_name='citas')
    estado = models.ForeignKey(
        ECita, on_delete=models.PROTECT, null=True, blank=True)
    tipo = models.ForeignKey(
        TCita, on_delete=models.PROTECT, null=True, blank=True)
    observaciones = models.CharField(max_length=250, null=True, blank=True)
    calendario = models.ForeignKey(Calendario, on_delete=models.PROTECT)
    # 6 = Sunday, 6= Monday ....
    dia_semana = models.IntegerField(null=True, blank=True)
    # guardamos el horario 9:00 => 0, 10:00 =>1, 11:00 => 2 ....
    posicion_turno = models.IntegerField(default=0)
    recurrente = models.BooleanField(default=0)
    extendedProps = models.ForeignKey(
        'cita.EventExtendedProp', null=True, blank=True, related_name='events', on_delete=models.PROTECT)
    color = models.CharField(max_length=20, default="#99ADC1")

    def __str__(self):
        return "{} {} {} {} ".format(self.fecha_inicio, self.paciente, self.estado, self.tipo)


class EventExtendedProp(models.Model):
    doctor = models.IntegerField()
    nombre_doctor = models.CharField(max_length=200, default="Dr.")
    cita = models.IntegerField(null=True, blank=True)
    evento_inicio = models.DateTimeField(null=True, blank=True)
    evento_fin = models.DateTimeField(null=True, blank=True)
