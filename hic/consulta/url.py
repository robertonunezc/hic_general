from django.conf.urls import url
from hic.consulta import views

urlpatterns = [
     url(r'^nueva/$', views.nueva_consulta, name='nueva_consulta'),
     url(r'^listado/$', views.listado_consultas, name='listado_consultas'),
     url(r'^editar/(?P<consulta_id>.+)$', views.editar_consulta, name='editar_consulta'),
 ]