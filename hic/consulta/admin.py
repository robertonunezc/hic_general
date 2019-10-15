from django.contrib import admin

# Register your models here.
from hic.consulta.models import TConsulta, TSignoVital

admin.site.register(TConsulta)
admin.site.register(TSignoVital)
