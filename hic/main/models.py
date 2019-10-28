from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from cloudinary.models import CloudinaryField
from django.conf import settings


# Create your models here.


class Usuario(AbstractUser):
    objects = UserManager()


class Persona(models.Model):
    MASCULINO = 0
    FEMENINO = 1
    GENERO = (
        (MASCULINO, "MASCULINO"),
        (FEMENINO, "FEMENINO")
    )
    nombre = models.CharField(max_length=80)
    primer_apellido = models.CharField(max_length=80)
    segundo_apellido = models.CharField(max_length=80)
    telefono = models.CharField(max_length=80, unique=True)
    genero = models.IntegerField(choices=GENERO)
    fecha_nacimiento = models.DateField(null=False, blank=False)

    def get_full_name(self):
        full_name = '%s %s %s' % (self.nombre, self.primer_apellido, self.segundo_apellido)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name().strip()


class Paciente(Persona):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, blank=True)


class Institucion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)


class Medico(Persona):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    cedula = models.CharField(max_length=80, unique=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.SET_NULL, null=True)


class Especialidad(models.Model):
    nombre = models.CharField(null=False, unique=True, max_length=80)

    def __str__(self):
        return self.nombre


class EspecialidadMedico(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='especialidades')


class NEstado(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class NMunicipio(models.Model):
    nombre = models.CharField(max_length=80)
    estado = models.ForeignKey(NEstado, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class NCodigoPostal(models.Model):
    codigo = models.CharField(max_length=80, unique=True)
    municipio = models.ForeignKey(NMunicipio, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo


class NColonia(models.Model):
    nombre = models.CharField(max_length=80)
    codigo_postal = models.ForeignKey(NCodigoPostal, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Direccion(models.Model):
    calle = models.CharField(max_length=250)
    numero_ext = models.CharField(max_length=250)
    numero_int = models.CharField(max_length=250, null=True, blank=True)
    colonia = models.CharField(max_length=250, null=True, blank=True)
    codigo_postal = models.ForeignKey(NColonia, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)


class Consultorio(models.Model):
    nombre = models.CharField(max_length=80)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=80)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
