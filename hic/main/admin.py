from django.contrib import admin
from hic.main.models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Especialidad)
# admin.site.register(EspecialidadMedico)
admin.site.register(NEstado)
admin.site.register(Institucion)
admin.site.register(NCodigoPostal)
admin.site.register(NMunicipio)
