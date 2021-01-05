from django.urls import path
from hic.consulta import views
app_name = 'consulta'
urlpatterns = [
    path('nueva/', views.nueva_consulta, name='nueva_consulta'),
    path('listado/', views.listado_consultas, name='listado_consultas'),
    path('editar/<int:consulta_id>', views.editar_consulta, name='editar_consulta'),
 ]