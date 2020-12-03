from django.db import models

from hic.main.models import Medico, Paciente


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
    INICIAL = 1
    SEGUIMIENTO = 2

    TIPO = (
        (INICIAL, "INICIAL"),
        (SEGUIMIENTO, "SEGUIMIENTO"),
    )

    tipo = models.IntegerField(choices=TIPO, unique=True)

    def __str__(self):
        for item in self.TIPO:
            if item[0] == self.tipo:
                return item[1]
        return self.tipo


class Cita(models.Model):
    fecha = models.DateTimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    estado = models.ForeignKey(ECita, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TCita, on_delete=models.PROTECT)
    observaciones = models.CharField(max_length=250, null=True, blank=True)
    calendario = models.ForeignKey(Calendario, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {} {} {} ".format(self.fecha, self.paciente, self.estado, self.tipo)


class Event(models.Model):
    titulo = models.CharField(max_length=100, default="Horario de Consulta")
    descripcion = models.CharField(max_length=200, default="")
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    dia_semana = models.IntegerField()
    # 0 Block event, 1 Pacient date event
    # tipo = models.IntegerField(default=0)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, null=True, blank=True)
    calendario = models.ForeignKey('cita.Calendario', related_name='eventos', on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="#3788d8")

    def __str__(self):
        return "{} {}".format(self.titulo, self.medico.nombre)

    def save(self, *args, **kwargs):
        if self.cita is not None:
            self.color = "#2cb67d"
        super(Event, self).save(*args, **kwargs)
