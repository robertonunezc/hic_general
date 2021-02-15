from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hic.cita.models import Event, Calendario, EventExtendedProp
from hic.cita.serializer import EventoSerializer, EventExtendedPropSerializer
from hic.main import process_inital_data
from hic.main.models import Medico, NEstado, NMunicipio, NCodigoPostal, \
    NColonia
from hic.main.serializer import SpecialistSerializer
from hic.paciente.forms import MedicoForm
from django.views.decorators.csrf import csrf_exempt
import json
import openpyxl
import datetime

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

        dia_semana = datetime.datetime.strptime(request.POST.get('date'), "%Y-%m-%dT%H:%M:%S").date().weekday()

        if dia_semana == 6:
            dia_semana = 0
        else:
            dia_semana += 1
        print(dia_semana)
        # date_end = date + datetime.timedelta(days=1)
        events = Event.objects.filter(dia_semana=dia_semana, tipo=0, deshabilitado=0)
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
    eventos = Event.objects.filter(tipo=0, deshabilitado=0)  # TODO only load the current month
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
    try:
        if request.method == "POST":
            specialist_id = request.POST.get('doctor')
            start_time = request.POST.get('inicio-cita-especialista')
            end_time = request.POST.get('fin-cita-especialista')
            recuerrente_si = request.POST.get('eventoRecurrente')
            recuerrente = True if recuerrente_si == "recurrente" else False
            dia_semana = datetime.datetime.strptime(start_time, "%Y-%m-%d").date().weekday()

            if dia_semana == 6:
                dia_semana = 0
            else:
                dia_semana += 1

            specialist = Medico.objects.get(pk=specialist_id)
            event = Event()
            event.titulo = specialist.nombre
            event.hora_inicio = start_time
            event.hora_fin = end_time
            event.calendario = Calendario.objects.first()
            event.medico = specialist
            event.recurrente = recuerrente
            event.dia_semana = dia_semana
            event.tipo = 0
            event.save()
            extended_props = EventExtendedProp()
            extended_props.evento = event.pk
            extended_props.doctor = specialist.pk
            extended_props.save()

            event.extendedProps = extended_props
            event.save()

            return redirect('main:horarios_especialista')

    except Exception as e:
        messages.add_message(request=request, level=messages.ERROR,
                             message="Ha ocurrido un error. Intente nuevamente. Todos los datos son obligatorios")
        return redirect('main:horarios_especialista')

    return HttpResponse("Acceso denegado")

@login_required
def borrar_evento_horario(request,event_id):
    if request.method == 'POST':
        try:
            evento = Event.objects.get(pk=event_id)
            evento.deshabilitado = True
            evento.save()
            return redirect('main:listado_medicos')
        except Event.DoesNotExist:
            print("No existe")
        except Exception as e:
            print(e)
    return render(request,'cita/confirmacion_borrar.html')

@login_required
def cargar_eventos(request):
    try:
        response = []
        eventos = Event.objects.filter(tipo=0, deshabilitado=0)  # TODO only load the current month

        for evento in eventos:
            if evento.recurrente:
                evento_dict = {
                    'startRecur': datetime.datetime.strftime(evento.hora_inicio, '%Y-%m-%dT%H:%M:%S%z'),
                    'daysOfWeek': [evento.dia_semana],
                    'startTime': str(evento.hora_inicio.time()),
                    'endTime': str(evento.hora_fin.time()),
                    'title': evento.titulo,
                    'backgroundColor': evento.color,
                    'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data
                }
            else:
                # TODO falta el cargar eventos sencillo
                evento_dict = {
                    'title': evento.titulo,
                    'backgroundColor': evento.color,
                    'start': str(evento.hora_inicio),
                    'end': str(evento.hora_fin),
                    'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data

                }
            response.append(evento_dict)

    except Event.DoesNotExist:
        print("Evento does not exist")
        response = {'rc': 500, 'msg': 'Error loading Events', 'data': None}

    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def nuevo_medico(request):
    form = MedicoForm()
    error= None
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('especialistas/listado')

        else:
            error = "Por favor revise los datos proporcionados algunos son incorrectos"
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'medico/nuevo_medico.html', context=context)


@login_required
def editar_medico(request, especialista_id):
    medico = get_object_or_404(Medico, pk=especialista_id)
    form = MedicoForm(instance=medico)
    msg = None
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            msg = "Especialista editado con éxito"
            messages.add_message(request=request, level=messages.ERROR,
                                 message=msg)
            return  redirect('main:listado_medicos')

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'medico/editar_medico.html', context=context)


@login_required
def import_initial_data(request):
    error = None
    if request.method == 'POST':
        file = request.FILES['initial-data']
        if process_inital_data.validate_file_extension(filename=file.name):
            try:
                raw_data = process_inital_data.process_file(file=file,sheet="LISTADO")
                process_inital_data.process_data(data=raw_data)
            except Exception as e:
                print(e)
                error = e
        else:
            error = "El archivo no tiene el formato correcto"
    context = {
        'error': error
    }
    return render(request, 'import_initial_data.html', context=context)


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


def first_tenant(request):
    from customer.models import Client

    # create your public tenant
    tenant = Client(domain_url='playa.cisnemexico.org',schema_name='playaok',name='SucursalPlayaOK',plan='ANUAL',started_date='2020-12-12')
    tenant.save()
