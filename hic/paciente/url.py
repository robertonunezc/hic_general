from django.conf.urls import url
from hic.paciente import views

urlpatterns = [
     url(r'^listado/$', views.listado_paciente, name='listado_pacientes'),
     url(r'^nuevo/$', views.nuevo_paciente, name='nuevo_paciente'),
     url(r'^editar/(?P<paciente_id>.+)$', views.editar_paciente, name='editar_paceinte'),
     url(r'^pdf/(?P<paciente_id>.+)$', views.ver_pdf_historia, name='ver_pdf_historia'),
     url(r'^historia/(?P<paciente_id>.+)$', views.historia_clinica, name='historia_clinica'),
 ]
