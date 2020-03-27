import openpyxl
import  json
import dateutil.parser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
from hic.cita.models import Calendario, Event
from hic.main.models import Medico, Usuario, Especialidad, EspecialidadMedico, NEstado, NMunicipio, NCodigoPostal, \
    NColonia
from hic.paciente.forms import MedicoForm, ConsultorioForm, DireccionForm
import json

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


@login_required
def nuevo_medico(request):
    form = MedicoForm()
    consultorio_form = ConsultorioForm()
    direccion_form = DireccionForm()
    error= None
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        consultorio_form = ConsultorioForm(request.POST)
        direccion_form = DireccionForm(request.POST)
        if form.is_valid() and consultorio_form.is_valid() and direccion_form.is_valid():
            medico = form.save()
            calendario = Calendario()
            calendario.medico = medico
            calendario.save()
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
            consultorio = consultorio_form.save(commit=False)
            direccion = direccion_form.save()
            consultorio.medico = medico
            consultorio.direccion = direccion
            consultorio.save()

            #events
            jdata = json.loads(json.loads(request.POST.get('calendar')))
            for val in jdata:
                for day in val['daysOfWeek']:
                    event = Event()
                    event.titulo = val['title']
                    event.tipo = 0 if val['type'] == 'block' else 1
                    event.hora_inicio = dateutil.parser.parse(val['startTime'])
                    event.hora_fin = dateutil.parser.parse(val['endTime'])
                    event.dia_semana = day
                    event.calendario = calendario
                    event.save()
            response = {'rc': 200, 'msg': 'Medico guardado', 'data': {}}
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            error = "Por favor revise los datos proporcionados algunos son incorrectos"
            response = {'rc': 500, 'msg': error, 'data': {}}
            return HttpResponse(json.dumps(response), content_type='application/json')
    context = {
        'form': form,
        'consultorio_form': consultorio_form,
        'direccion_form': direccion_form,
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

