from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from cloudinary.models import CloudinaryField
from django.conf import settings
# Create your models here.

ESTADO_CITAS = (
    (0, 'Agendada'),
    (1, 'Confirmada'),
    (2, 'Cancelada'),
)

class Usuario(AbstractUser):
    objects = UserManager()
    telefono = models.IntegerField(blank=True, null=True)


class Paciente(models.Model):
    nombre = models.CharField(max_length=80)
    primer_apellido = models.CharField(max_length=80)
    segundo_apellido = models.CharField(max_length=80)
    fecha = models.DateField(null=True, blank=True)
    edad = models.IntegerField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)
    ta = models.CharField(max_length=50,blank=True, null=True)
    fc = models.CharField(max_length=50,blank=True, null=True)
    so2 = models.CharField(max_length=50,blank=True, null=True)
    antecedentes_patologicos = models.ManyToManyField('main.AntecendentesPatologicos')
    otros = models.TextField(null=True, blank=True)
    motivos_consulta = models.TextField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)
    indicaciones = models.TextField(null=True, blank=True)
    image = CloudinaryField('image',null=True, blank=True)

    def get_full_name(self):
        full_name = '%s %s %s' % (self.nombre, self.primer_apellido, self.segundo_apellido)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name().strip()


class AntecendentesPatologicos(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class TipoConsulta(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Consulta(models.Model):
    paciente = models.ForeignKey('main.Paciente', related_name='consultas')
    fecha = models.DateField(auto_now_add=True)
    indicaciones = models.TextField(null=True, blank=True)
    doctor = models.IntegerField(choices=settings.DOCTORES)
    pagado = models.BooleanField(default=False)
    costo = models.FloatField(default=0.0)
    tipo_consulta = models.ForeignKey('main.TipoConsulta', related_name='consultas')


class Citas(models.Model):
    paciente = models.ForeignKey('main.Paciente', related_name='citas')
    fecha = models.DateTimeField()
    estado = models.IntegerField(choices=ESTADO_CITAS, default=0)
    doctor = models.IntegerField(choices=settings.DOCTORES)
    tipo_consulta = models.ForeignKey('main.TipoConsulta', related_name='citas')

