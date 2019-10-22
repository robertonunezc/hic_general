from django.db import models

from hic.main.models import Medico, Paciente


class SHorarioConsulta(models.Model):
    duracion = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()


class Calendario(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    horario_consulta = models.OneToOneField(SHorarioConsulta)

    def __str__(self):
        return self.medico.__str__()


class TDia(models.Model):
    DOMINGO = 0
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6

    SEMANA = (
        (DOMINGO, "DOMINGO"),
        (LUNES, "LUNES"),
        (MARTES, "MARTES"),
        (MIERCOLES, "MIERCOLES"),
        (JUEVES, "JUEVES"),
        (VIERNES, "VIERNES"),
        (SABADO, "SABADO"),
    )

    dia = models.IntegerField(choices=SEMANA, unique=True)

    def __str__(self):
        for item in self.SEMANA:
            if item[0] == self.dia:
                return item[1]
        return self.dia


class SHorarioConsultaDias(models.Model):
    s_horario_consulta = models.ForeignKey(SHorarioConsulta, on_delete=models.CASCADE)
    dia = models.ForeignKey(TDia, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)


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
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey(ECita, on_delete=models.SET_NULL, null=True)
    tipo = models.ForeignKey(TCita, on_delete=models.SET_NULL, null=True)
    calendario = models.ForeignKey(Calendario, on_delete=models.SET_NULL, null=True)
