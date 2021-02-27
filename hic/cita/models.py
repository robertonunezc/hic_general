from django.db import models

from hic.main.models import Medico, Paciente
import json
from colorfield.fields import ColorField

class Calendario(models.Model):
    nombre = models.CharField(max_length=200, default="Clínica General")
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)

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
    fecha = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name='citas')
    estado = models.ForeignKey(ECita, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TCita, on_delete=models.PROTECT)
    observaciones = models.CharField(max_length=250, null=True, blank=True)
    calendario = models.ForeignKey(Calendario, on_delete=models.PROTECT)
    deshabilitado = models.BooleanField(default=0) #0 habilitado, 1 dehabilitado
    pagada = models.BooleanField(default=0) #0 no pagada, 1 pagada
    def __str__(self):
        return "{} {} {} {} ".format(self.fecha, self.paciente, self.estado, self.tipo)


class Event(models.Model):
    titulo = models.CharField(max_length=100, default="Horario de Consulta")
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    # 0 Specialist event, 1 Pacient date event
    tipo = models.IntegerField(default=0)
    recurrente = models.BooleanField(default=0) #1 recurrent, 0 not
    dia_semana = models.IntegerField(null=True, blank=True) # 0 = Sunday, 1= Monday ....
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    calendario = models.ForeignKey('cita.Calendario', related_name='eventos', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="#3788d8")
    extendedProps = models.ForeignKey('cita.EventExtendedProp', null=True, blank=True,
                                       related_name='events', on_delete=models.PROTECT)
    deshabilitado = models.BooleanField(default=0) #0 habilitado, 1 dehabilitado

    def __str__(self):
        if self.tipo == 0:
            return "{} {}".format(self.titulo, self.medico.nombre)
        if self.tipo == 1 and self.cita is not None:
            return "{} {}".format(self.titulo, self.cita.paciente.nombre)
        return self.titulo

class EventExtendedProp(models.Model):
    doctor = models.IntegerField()
    cita = models.IntegerField(null=True, blank=True)
    evento = models.IntegerField(null=True, blank=True)