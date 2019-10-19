from django.conf.urls import url
from hic.main import views

urlpatterns = [
    url(r'^/', views.inicio, name='menu_principal'),
    url(r'^medicos/listado', views.listado_medicos, name='listado_medicos'),
    url(r'^medicos/nuevo', views.nuevo_medico, name='nuevo_medico'),
]
