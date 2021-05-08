from django.urls import path
from hic.cita import views

app_name = 'cita'
urlpatterns = [
    path('horario/', views.seleccionar_horario, name='seleccionar_horario'),
    path('cargar/eventos/', views.cargar_eventos, name='cargar_eventos'),
    path('calendario/registrar/cita/', views.calendario_registrar_cita,
         name='calendario_registrar_cita'),
    path('tipo-cita/<int:horario_id>', views.seleccionar_tipo_cita,
         name='seleccionar_tipo_cita'),
    path('borrar/<int:cita_id>', views.borrar_cita, name='borrar_cita'),
    path('detalle/<int:cita_id>', views.detalle_cita, name='detalle_cita'),
    path('nueva/', views.nueva_cita, name='nueva_cita'),
    path('primera/', views.primera_nueva_cita, name='primera_cita'),
    path('editar/<int:cita_id>', views.editar_cita, name='editar_cita'),
    path('listado/', views.listado_citas, name='listado_citas'),
    path('migrar/', views.migrar, name='migrar'),
    path('migrarcolores/', views.migrar_color_evento, name='migrar_color_evento'),
]
