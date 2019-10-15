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
    telefono = models.IntegerField(blank=False, null=False)
    genero = models.IntegerField(choices=GENERO)
    fecha_nacimiento = models.DateField(null=False, blank=False)

    def get_full_name(self):
        full_name = '%s %s %s' % (self.nombre, self.primer_apellido, self.segundo_apellido)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name().strip()


class Paciente(Persona):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.usuario


class Medico(Persona):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.usuario


class TEspecialidad(models.Model):
    nombre = models.CharField(null=False, unique=True, max_length=80)


class EspecialidadMedico(models.Model):
    especialidad = models.ForeignKey(TEspecialidad, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
