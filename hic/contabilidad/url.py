from django.urls import path
from hic.contabilidad import views
app_name = 'contabilidad'
urlpatterns = [
    path('gastos', views.listado_gastos, name='listado_gastos'),
    path('gastos/nuevo', views.nuevo_gasto, name='nuevo_gastos'),
    path('gastos/editar/<int:gasto_id>',
         views.editar_gasto, name='editar_gastos'),
    path('servicio/detalle/<int:servicio_id>',
         views.detalle_servicio, name='obtener_servicio'),
    path('agregar/servicio/paciente/<int:servicio_id>/<int:paciente_id>',
         views.agregar_servicio_paciente, name='agregar_servicio_paciente'),
]
