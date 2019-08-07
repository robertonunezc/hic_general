from django.conf.urls import url
from hic.paciente import views

urlpatterns = [
     url(r'^listado/$', views.listado, name='listado_pacientes'),
     url(r'^nuevo/$', views.nuevo, name='nuevo_paciente'),
     url(r'^editar/(?P<paciente_id>.+)$', views.editar, name='editar_paceinte'),
     url(r'^pdf/(?P<paciente_id>.+)$', views.ver_pdf_historia, name='ver_pdf_historia'),
     url(r'^historia/(?P<paciente_id>.+)$', views.historia_clinica, name='historia_clinica'),
 ]