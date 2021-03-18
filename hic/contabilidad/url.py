from django.urls import path
from hic.contabilidad import views
app_name = 'contabilidad'
urlpatterns = [
     path('gastos', views.listado_gastos, name='listado_gastos'),
     path('gastos/nuevo', views.nuevo_gasto, name='nuevo_gastos'),
     path('gastos/editar/<int:gasto_id>', views.editar_gasto, name='editar_gastos'),
 ]
