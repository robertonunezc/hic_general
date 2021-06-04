from django.contrib import admin

# Register your models here.
from hic.cita.models import ECita, TCita, Calendario, Cita, EventExtendedProp


class CitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha_inicio', 'tipo', 'updated_at']
    search_fields = ['paciente', 'fecha_inicio', 'tipo']
    list_filter = ['paciente', 'fecha_inicio', 'tipo']


admin.site.register(Calendario)
# admin.site.register(Event, EventAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(ECita)
admin.site.register(TCita)
admin.site.register(EventExtendedProp)
