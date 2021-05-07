from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hic.cita.models import Calendario, EventExtendedProp, Cita
from hic.cita.serializer import EventExtendedPropSerializer, CitaSerializer
from hic.main import process_inital_data
from hic.main.models import Medico, NEstado, NMunicipio, NCodigoPostal, \
    NColonia, RegistroIncidencias
from hic.main.serializer import SpecialistSerializer
from hic.main.utils import get_dia_semana, get_mes
from hic.paciente.forms import MedicoForm
from django.views.decorators.csrf import csrf_exempt
import json
import openpyxl
import datetime as datetime2
from datetime import datetime, timedelta


@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def listado_medicos(request):
    if request.user.groups.filter(name="terapeuta"):
        return redirect('/acceso-denegado/')
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

        dia_semana = datetime2.datetime.strptime(
            request.POST.get('date'), "%Y-%m-%dT%H:%M:%S").date().weekday()

        if dia_semana == 6:
            dia_semana = 0
        else:
            dia_semana += 1
        print(dia_semana)
        # date_end = date + datetime.timedelta(days=1)
        events = ""
        specilists = []
        for event in events:
            specilists.append(event.medico)
        serializer = SpecialistSerializer(specilists, many=True)
        response = {'rc': 200, 'msg': 'Specialists', 'data': serializer.data}
    except Exception as e:
        print(e)
        response = {'rc': 500,
                    'msg': 'Error loading Specialists', 'data': None}
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def configurar_horario_medico(request):
    especialistas = Medico.objects.all()
    context = {
        'especialistas': especialistas
    }
    return render(request, 'medico/seleccionar_horario.html', context=context)


@login_required
def assing_specialist_consult_time(request):
    if request.user.groups.filter(name="terapeuta"):
        return redirect('/acceso-denegado/')
    try:
        if request.method == "POST":
            specialist_id = request.POST.get('doctor')
            start_time = request.POST.get('inicio-cita-especialista')
            end_time = request.POST.get('fin-cita-especialista')
            recuerrente_si = request.POST.get('eventoRecurrente')
            recuerrente = True if recuerrente_si == "recurrente" else False
            dia_semana = datetime2.datetime.strptime(
                start_time, "%Y-%m-%d").date().weekday()
            print(dia_semana)

            start_time = datetime.strptime(str(start_time), "%Y-%m-%d")
            specialist = Medico.objects.get(pk=specialist_id)

            for i in range(0, 52):
                if i > 0:
                    days = 7 * i
                    new_start_time = start_time + timedelta(days=days)
                else:
                    new_start_time = start_time

                posicion_turno = 0
                for time in range(9, 21):
                    cita = Cita()
                    cita.titulo = specialist.nombre
                    cita.fecha_inicio = new_start_time + timedelta(hours=time)
                    cita.fecha_fin = new_start_time + timedelta(hours=time + 1)
                    cita.calendario = Calendario.objects.first()
                    cita.medico = specialist
                    cita.recurrente = recuerrente
                    cita.dia_semana = dia_semana
                    cita.posicion_turno = posicion_turno
                    cita.save()
                    posicion_turno += 1

                    extended_props = EventExtendedProp()
                    extended_props.cita = cita.pk
                    extended_props.doctor = specialist.pk
                    extended_props.nombre_doctor = specialist.nombre
                    extended_props.evento_inicio = cita.fecha_inicio
                    extended_props.evento_fin = cita.fecha_fin
                    extended_props.save()

                    cita.extendedProps = extended_props
                    cita.save()
                if not recuerrente:
                    break
            return redirect('main:horarios_especialista')

    except Exception as e:
        print(e)
        messages.add_message(request=request, level=messages.ERROR,
                             message="Ha ocurrido un error. Intente nuevamente. Todos los datos son obligatorios")
        return redirect('main:horarios_especialista')

    return HttpResponse("Acceso denegado")


@login_required
def borrar_evento_horario(request, event_id):
    if not request.user.is_superuser:
        return redirect('/acceso-denegado/')
    cita = Cita.objects.get(pk=event_id)
    try:
        usuario = request.user
        if request.method == 'POST':
            recuerrente_si = request.POST.get('eventoRecurrente')
            borrado_recuerrente = True if recuerrente_si == "si-recurrente" else False
        #     print("Evento recurrente {}".format(recuerrente_si))
            if borrado_recuerrente:
                dia_semana = cita.dia_semana  # 0->Mon, 1->Tuesday...6->Sunday
                medico = cita.medico
                cita_id = cita.pk
                espacios_medico = Cita.objects.filter(
                    dia_semana=dia_semana, medico=medico)
                espacios_medico.delete()
            else:
                cita.delete()
            return redirect('main:horarios_especialista')
    except Exception as e:
        print(e)

    context = {'cita': cita, 'dia_semana': "", 'mes': ""}
    return render(request, 'medico/confirmacion_borrar.html', context=context)


@login_required
def cargar_eventos(request):
    try:
        response = []
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)
        if start_date is None and end_date is None:
            start_date = datetime.today()
            end_date = datetime.today() + timedelta(days=1)
        print("Start Loading events")
        eventos = Cita.objects.filter(fecha_inicio__gte=start_date,
                                      fecha_fin__lte=end_date).order_by('id')
        print("End Loading events")
        for evento in eventos:
            evento_dict = {
                'title': evento.titulo,
                'backgroundColor': evento.color,
                'start': str(evento.fecha_inicio),
                'end': str(evento.fecha_fin),
                'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data
            }

            response.append(evento_dict)

    except Cita.DoesNotExist:
        print("Cita does not exist")
        response = {'rc': 500, 'msg': 'Error loading Events', 'data': None}

    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def nuevo_medico(request):
    form = MedicoForm()
    error = None
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:listado_medicos')

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
            return redirect('main:listado_medicos')

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
                raw_data = process_inital_data.process_file(
                    file=file, sheet="LISTADO")
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


@login_required
def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')


def save_incidencia_log(cita):
    """Save incident LOG"""
    incidencia = RegistroIncidencias()
    incidencia.accion = "Borrado cita {} {} {}".format(
        cita_borrar.paciente.nombre, cita_borrar.medico.nombre, cita_borrar.fecha_inicio)
    incidencia.comentario = motivo
    incidencia.usuario = usuario
    incidencia.save()


# cargar colonias(dev)
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

                obj_estado, created = NEstado.objects.get_or_create(
                    nombre=estado)
                obj_municipio, created = NMunicipio.objects.get_or_create(
                    estado=obj_estado, nombre=municipio)
                obj_cp, created = NCodigoPostal.objects.get_or_create(
                    municipio=obj_municipio, codigo=cp)
                obj_colonia, created = NColonia.objects.get_or_create(
                    codigo_postal=obj_cp, nombre=colonia)
    return render(request, 'carga.html')


def first_tenant(request):
    from customer.models import Client

    # create your public tenant
    tenant = Client(domain_url='playa.cisnemexico.org', schema_name='playaok', name='SucursalPlayaOK', plan='ANUAL',
                    started_date='2020-12-12')
    tenant.save()


def test(request):
    print("Start")
    eventos = Event.objects.all()

    print("end")
    return HttpResponse("Loaded{}".format(eventos.count()))
