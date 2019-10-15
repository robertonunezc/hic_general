from django.contrib import admin

# Register your models here.
from hic.cita.models import TFrecuenciaRepeticion, ECita, TCita

admin.site.register(TFrecuenciaRepeticion)
admin.site.register(ECita)
admin.site.register(TCita)
