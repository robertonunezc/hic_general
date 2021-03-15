from django.urls import path
from hic.contabilidad import views
app_name = 'contabilidad'
urlpatterns = [
     path('gastos', views.listado_gastos, name='listado_gastos'),
 ]
