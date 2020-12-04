from django.urls import path
from hic.cita import views

app_name = 'cita'
urlpatterns = [
    path('horario/', views.seleccionar_horario, name='seleccionar_horario'),
    path('calendario/registrar/cita/', views.calendario_registrar_cita, name='calendario_registrar_cita'),
    path('tipo-cita/<int:horario_id>', views.seleccionar_tipo_cita, name='seleccionar_tipo_cita'),
    path('nueva/', views.nueva_cita, name='nueva_cita'),
    path('primera/', views.primera_nueva_cita, name='primera_cita'),
    path('editar/<int:cita_id>', views.editar_cita, name='editar_cita'),
    path('listado/', views.listado_citas, name='listado_citas'),
]
