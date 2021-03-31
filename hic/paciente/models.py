from django.db import models

from hic.main.models import Paciente, Medico


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='historia_clinica')
    fecha = models.DateField()
    folio = models.IntegerField()
    nombre_madre = models.CharField(max_length=400,null=True, blank=True)
    ocupacion_madre = models.CharField(max_length=400 ,null=True, blank=True)
    telefono_madre = models.CharField(max_length=400,null=True, blank=True)
    nombre_padre = models.CharField(max_length=400, null=True, blank=True)
    ocupacion_padre = models.CharField(max_length=400 ,null=True, blank=True)
    telefono_padre = models.CharField(max_length=400,null=True, blank=True)
    estado_civil = models.CharField(max_length=400, null=True, blank=True)
    escolaridad_menor = models.CharField(max_length=400, null=True, blank=True)
    nombre_colegio = models.CharField(max_length=400 ,null=True, blank=True)
    grado_cursa = models.CharField(max_length=400 ,null=True, blank=True)
    diagnostico_medico = models.TextField(null=True, blank=True)
    motivo_consulta = models.TextField(null=True, blank=True)
    observaciones_generales = models.TextField(null=True, blank=True)
    remitido_por = models.CharField(max_length=400, null=True, blank=True)
    servicio_solicitado = models.CharField(max_length=400, null=True, blank=True)
    """Informacion administrativa"""
    terapia_fisica = models.BooleanField(default=False)
    terapia_ocupacional = models.BooleanField(default=False)
    psicologia = models.BooleanField(default=False)
    neuropsicologia = models.BooleanField(default=False)
    psicopedagogia = models.BooleanField(default=False)
    terapia_lenguaje = models.BooleanField(default=False)
    neuroterapia = models.BooleanField(default=False)
    fecha_cita = models.DateField(null=True, blank=True)
    profesional_cargo = models.CharField(max_length=250, null=True, blank=True)
    costo_valoracion = models.CharField(max_length=250, default=0, null=True, blank=True)
    costo_terapias = models.CharField(max_length=250, default=0)
    nombre_entrevistador = models.CharField(max_length=250, null=True, blank=True)



class TAlergia(models.Model):
    nombre = models.CharField(max_length=80, unique=True)


class AntecedenteAlergia(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.SET_NULL, null=True)
    alergia = models.ForeignKey(TAlergia, on_delete=models.SET_NULL, null=True)