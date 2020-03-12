from django.contrib import admin

# Register your models here.
from hic.cita.models import ECita, TCita


admin.site.register(ECita)
admin.site.register(TCita)
