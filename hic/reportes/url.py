from django.urls import path
from hic.reportes import views
app_name = 'reportes'
urlpatterns = [
     path('citas', views.estado_citas, name='reporte_citas'),
 ]
