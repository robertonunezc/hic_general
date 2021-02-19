from django.shortcuts import render

# Create your views here.
from hic.cita.models import ECita, Cita
from hic.main.models import Medico


def estado_citas(request):
    estados_citas = ECita.objects.all()
    especialistas = Medico.objects.all()
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio', None)
        fecha_fin = request.POST.get('fecha_fin', None)
        if fecha_inicio is None or fecha_fin is None:
            message = "Debe ingresar los datos de fecha"
            return render(request, 'reportes/listado_citas.html', context={'mensaje': message})

        citas = Cita.objects.filter(fecha__gte=fecha_inicio, fecha_fin__lte=fecha_fin, deshabilitado=0)
        estado_id = request.POST['estado']
        especialista_id = request.POST['especialista']
        if estado_id != "-1":
            citas = citas.filter(estado_id=estado_id)
        if especialista_id != "-1":
            citas = citas.filter(medico_id=especialista_id)
        context = {
            'citas': citas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        }
        return render(request, 'reportes/listado_citas.html', context=context)

    context = {
        'estados': estados_citas,
        'especialistas': especialistas
    }
    return render(request, 'reportes/rango_fechas_reporte.html', context=context)
