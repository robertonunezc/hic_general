from django.urls import path
from hic.cita import views

app_name = 'cita'
urlpatterns = [
    path('nueva/', views.nueva_cita, name='nueva_cita'),
    path('primera/', views.primera_nueva_cita, name='primera_nueva_cita'),
    path('editar/<int:cita_id>', views.editar_cita, name='editar_cita'),
    path('listado/', views.listado_citas, name='listado_citas'),
]
