from django.contrib import admin

# Register your models here.
from hic.cita.models import ECita, TCita, Calendario, Event, Cita, EventExtendedProp

admin.site.register(Calendario)
# admin.site.register(Event)
admin.site.register(Cita)
admin.site.register(ECita)
admin.site.register(TCita)
# admin.site.register(EventExtendedProp)
