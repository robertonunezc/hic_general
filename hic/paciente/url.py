from django.urls import path
from hic.paciente import views
app_name = 'pacientes'
urlpatterns = [
    path('listado/', views.listado_paciente, name='listado_pacientes'),
    path('nuevo/', views.nuevo_paciente, name='nuevo_paciente'),
    path('agregar/servicios/<int:paciente_id>',
         views.agregar_servicios, name='agregar_servicios'),
    path('editar/<int:paciente_id>', views.editar_paciente, name='editar_paceinte'),
    path('pdf/<int:paciente_id>', views.ver_pdf_historia, name='ver_pdf_historia'),
    path('historia/<int:paciente_id>',
         views.historia_clinica, name='historia_clinica'),
    path('estado-cuenta/<int:paciente_id>',
         views.estado_cuenta, name='estado_cuenta'),
]
