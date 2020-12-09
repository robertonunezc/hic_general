from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hic.cita.models import Event, Calendario, EventExtendedProp
from hic.cita.serializer import EventoSerializer
from hic.main.models import Medico, Especialidad, NEstado, NMunicipio, NCodigoPostal, \
    NColonia, EspecialidadMedico
from hic.main.serializer import SpecialistSerializer
from hic.paciente.forms import MedicoForm
from django.views.decorators.csrf import csrf_exempt
import json
import openpyxl
import datetime
import pytz

@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def listado_medicos(request):
    medicos = Medico.objects.all()
    context = {
        'medicos': medicos
    }
    return render(request, 'medico/listado_medicos.html', context=context)

@csrf_exempt
@login_required
def get_specialists_by_date(request):
    try:
        print(request.POST.get('date'))

        date = datetime.datetime.strptime(request.POST.get('date'),"%Y-%m-%dT%H:%M:%S%z").date()

        date_end = date + datetime.timedelta(days=1)
        events = Event.objects.filter(hora_inicio__gte=date, hora_fin__lte=date_end, tipo=0)
        specilists = []
        for event in events:
            specilists.append(event.medico)
        serializer = SpecialistSerializer(specilists, many=True)
        response = {'rc': 200, 'msg': 'Specialists', 'data': serializer.data}
    except Exception as e:
        print(e)
        response = {'rc': 500, 'msg': 'Error loading Specialists', 'data': None}
    return HttpResponse(json.dumps(response), content_type='application/json')

@login_required
def configurar_horario_medico(request):
    eventos = Event.objects.filter(tipo=0)  # TODO only load the current month
    serializer = EventoSerializer(eventos, many=True)
    especialistas = Medico.objects.all()
    # serializer.data['extendedProps'] = serializer.data['extended_props']
    print(serializer.data)
    context = {
        'eventos': json.dumps(serializer.data),
        'especialistas': especialistas
    }
    print(context)
    return render(request, 'medico/seleccionar_horario.html', context=context)


@login_required
def assing_specialist_consult_time(request):
    if request.method == "POST":
        specialist_id = request.POST.get('doctor')
        start_time = request.POST.get('inicio-cita-especialista')
        end_time = request.POST.get('fin-cita-especialista')

        specialist = Medico.objects.get(pk=specialist_id)
        event = Event()
        event.titulo = "Disponible-{}". format(specialist.nombre)
        event.hora_inicio = start_time
        event.hora_fin = end_time
        event.calendario = Calendario.objects.first()
        event.medico = specialist
        event.tipo = 0
        event.save()
        extended_props = EventExtendedProp()
        extended_props.evento = event.pk
        extended_props.doctor = specialist.pk
        extended_props.save()

        event.extendedProps = extended_props
        event.save()

        return redirect('main:horarios_especialista')

    return HttpResponse("Acceso denegado")




@login_required
def nuevo_medico(request):
    form = MedicoForm()
    error= None
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            medico = form.save()
            especialidades = form.cleaned_data.get('especialidades')
            for id in especialidades:
                try:
                    especialidad = Especialidad.objects.get(pk=id)
                    especialidad_medico = EspecialidadMedico()
                    especialidad_medico.especialidad = especialidad
                    especialidad_medico.medico = medico
                    especialidad_medico.save()
                except Especialidad.DoesNotExist:
                    continue
            return HttpResponseRedirect('/inicio/medicos/listado/')

        else:
            error = "Por favor revise los datos proporcionados algunos son incorrectos"
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'medico/nuevo_medico.html', context=context)


@login_required
def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, pk=medico_id)
    form = MedicoForm(instance=medico)
    msg = None
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            msg = "Cita actualizada con éxito"

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'cita/editar_cita.html', context=context)


#cargar colonias(dev)
def cargar_colonias(request):
    if request.method == 'POST':
        file = request.FILES["excel_file"]
        work_box = openpyxl.load_workbook(file)
        sheets = work_box.sheetnames
        for i in range(24, len(sheets)):
            work_sheet = work_box[sheets[i]]
            row_list = list(work_sheet.rows)
            for j in range(1, len(row_list)):
                cp = str(row_list[j][0].value).strip()
                colonia = str(row_list[j][1].value).strip()
                municipio = str(row_list[j][3].value).strip()
                estado = str(row_list[j][4].value).strip()

                obj_estado, created = NEstado.objects.get_or_create(nombre=estado)
                obj_municipio, created = NMunicipio.objects.get_or_create(estado=obj_estado, nombre=municipio)
                obj_cp, created = NCodigoPostal.objects.get_or_create(municipio=obj_municipio, codigo=cp)
                obj_colonia, created = NColonia.objects.get_or_create(codigo_postal=obj_cp, nombre=colonia)
    return render(request, 'carga.html')

