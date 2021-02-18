from django.contrib import admin

# Register your models here.
from hic.cita.models import ECita, TCita, Calendario, Event, Cita, EventExtendedProp

class CitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'tipo']
    search_fields = ['paciente', 'fecha', 'tipo']
    list_filter = ['paciente', 'fecha', 'tipo']

class EventAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'hora_inicio', 'hora_fin', 'tipo', 'color', 'recurrente', 'dia_semana', 'medico']
    search_fields = ['titulo', 'hora_inicio', 'hora_fin', 'tipo', 'color', 'recurrente', 'dia_semana', 'medico']
    list_filter = ['titulo', 'hora_inicio', 'hora_fin', 'tipo', 'color', 'recurrente', 'dia_semana', 'medico']

admin.site.register(Calendario)
admin.site.register(Event)
admin.site.register(Cita)
admin.site.register(ECita)
admin.site.register(TCita)
admin.site.register(EventExtendedProp)
