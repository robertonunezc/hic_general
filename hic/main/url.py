from django.urls import path
from hic.main import views

app_name = 'main'

urlpatterns = [
    path('', views.inicio, name='menu_principal'),
    path('especialistas/listado', views.listado_medicos, name='listado_medicos'),
    path('especialistas/nuevo', views.nuevo_medico, name='nuevo_medico'),
    path('especialistas/cargar-eventos', views.cargar_eventos, name='cargar_eventos'),
    path('especialistas/horario', views.configurar_horario_medico, name='horarios_especialista'),
    path('especialistas/borrar-evento/<int:event_id>', views.borrar_evento_horario, name='borrar_evento_horario'),
    path('asignar/especialista/', views.assing_specialist_consult_time,
         name='assing_specialist_consult_time'),
    path('especialistas/dia', views.get_specialists_by_date, name='specialist_by_date'),
    path('carga/', views.cargar_colonias, name='carga'),
    path('first/', views.first_tenant, name='first_tenant'),
]
