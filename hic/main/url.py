from django.urls import path
from hic.main import views

app_name = 'main'

urlpatterns = [
    path('', views.inicio, name='menu_principal'),
    path('medicos/listado', views.listado_medicos, name='listado_medicos'),
    path('medicos/nuevo', views.nuevo_medico, name='nuevo_medico'),
    path('carga/', views.cargar_colonias, name='carga'),
]
