from django.db import models

from hic.main.models import Paciente, Medico


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='paciente')
    fecha = models.DateField()
    folio = models.CharField(max_length=50)
    nombre_madre = models.CharField(max_length=50)
    ocupacion_madre = models.CharField(max_length=50)
    telefono_madre = models.CharField(max_length=50)
    nombre_padre = models.CharField(max_length=50)
    ocupacion_padre = models.CharField(max_length=50)
    telefono_padre = models.CharField(max_length=50)
    estado_civil = models.CharField(max_length=50)
    escolaridad_menor = models.CharField(max_length=50)
    nombre_colegio = models.CharField(max_length=50)
    grado_cursa = models.CharField(max_length=50)
    diagnostico_medico = models.TextField(null=True, blank=True)
    motivo_consulta = models.TextField(null=True, blank=True)
    observaciones_generales = models.TextField(null=True, blank=True)
    remitido_por = models.CharField(max_length=50)
    servicio_solicitado = models.CharField(max_length=50)
    """Informacion administrativa"""
    terapia_fisica = models.BooleanField(default=False)
    terapia_ocupacional = models.BooleanField(default=False)
    psicologia = models.BooleanField(default=False)
    neuropsicologia = models.BooleanField(default=False)
    psicopedagogia = models.BooleanField(default=False)
    terapia_lenguaje = models.BooleanField(default=False)
    neuroterapia = models.BooleanField(default=False)
    fecha_cita = models.DateField()
    profesional_cargo = models.CharField(max_length=250)
    costo_valoracion = models.CharField(max_length=250)
    costo_terapias = models.CharField(max_length=250)
    nombre_entrevistador = models.CharField(max_length=250)



class TAlergia(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class AntecedenteAlergia(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.SET_NULL, null=True)
    alergia = models.ForeignKey(TAlergia, on_delete=models.SET_NULL, null=True)