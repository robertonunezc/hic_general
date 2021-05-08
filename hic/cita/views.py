from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hic.cita.forms import CitaForm, PrimeraCitaForm
from hic.cita.models import Cita, ECita, TCita, Calendario, EventExtendedProp
from hic.cita.serializer import CitaSerializer, EventExtendedPropSerializer
from hic.main.models import Paciente, Medico, Especialidad, RegistroIncidencias
from hic.main.utils import get_dia_semana, get_mes
from hic.paciente.forms import PacienteForm
import json


@login_required
def seleccionar_horario(request):
    pacientes = Paciente.objects.all()
    especialistas = Medico.objects.all()
    tipo_citas = TCita.objects.all()
    medico = request.GET.get('especialista', None)
    url_loadevents = '/citas/cargar/eventos/'
    fecha_evento = False

    if medico is not None:
        url_loadevents = '/citas/cargar/eventos/?especialista={}'.format(
            medico)

    # I use this variable to move the calendar to specific date after an event was created
    if request.session.get('fecha_evento_creado', False):
        fecha_evento = request.session.get('fecha_evento_creado', False)

    print("FechaEvento {}".format(fecha_evento))
    context = {
        'pacientes': pacientes,
        'especialistas': especialistas,
        'tipo_citas': tipo_citas,
        'url_loadevents': url_loadevents,
        'fecha_evento': fecha_evento

    }
    request.session['fecha_evento_creado'] = None
    return render(request, 'cita/seleccionar_horario.html', context=context)


@login_required
def borrar_cita(request, cita_id):
    if not request.user.is_superuser:
        return redirect('/acceso-denegado/')

    cita = Cita.objects.get(pk=cita_id)
    usuario = request.user
    if request.method == 'POST':
        recuerrente_si = request.POST.get('eventoRecurrente')
        motivo = request.POST.get("motivo")
        borrado_recuerrente = True if recuerrente_si == "si-recurrente" else False
        print("Evento recurrente {}".format(recuerrente_si))
        try:
            # Borrado recurrente
            if borrado_recuerrente:
                dia_semana = cita.dia_semana  # 0->Mon, 1->Tuesday...6->Sunday
                posicion_dia = cita.posicion_turno  # 9:00->0, 10:00->1 ...21:00->11
                medico = cita.medico
                cita_id = cita.pk
                citas_registradas = Cita.objects.filter(
                    dia_semana=dia_semana, posicion_turno=posicion_dia, medico=medico).exclude(fecha_inicio__lt=cita.fecha_inicio)
                for cita_registrada in citas_registradas:
                    delete_date(cita_borrar=cita_registrada,
                                motivo=motivo, usuario=usuario)
                return HttpResponseRedirect('/citas/horario')

            # Borrado 1 sola cita
            delete_date(cita_borrar=cita, motivo=motivo, usuario=request.user)
            messages.add_message(request=request, level=messages.SUCCESS,
                                 message="Cita borrada con exito. ")
            return HttpResponseRedirect('/citas/horario')

        except Cita.DoesNotExist:
            print("No existe")
            messages.add_message(request=request, level=messages.ERROR,
                                 message="Cita no existe. ")
        except Exception as e:
            print(e)
            messages.add_message(request=request, level=messages.ERROR,
                                 message="Error borrando la cita. ")
    context = {'cita': cita, 'dia_semana': cita.dia_semana}

    return render(request, 'cita/confirmacion_borrar.html', context=context)


def delete_date(cita_borrar, motivo, usuario):
    try:
        """Save incident LOG"""
        incidencia = RegistroIncidencias()
        incidencia.accion = "Borrado cita {} {} {}".format(
            cita_borrar.paciente.nombre, cita_borrar.medico.nombre, cita_borrar.fecha_inicio)
        incidencia.comentario = motivo
        incidencia.usuario = usuario
        incidencia.save()

        cita_borrar.titulo = "{} {}".format(
            cita_borrar.medico.nombre, cita_borrar.medico.primer_apellido)
        cita_borrar.color = "#99ADC1"
        cita_borrar.paciente = None
        cita_borrar.recurrente = False
        cita_borrar.save()

    except Exception as e:
        print(e)
        print("Error borrando citas")


@login_required
def cargar_eventos(request):
    try:
        response = []
        start_date = request.GET.get('start', None)
        end_date = request.GET.get('end', None)

        medico = request.GET.get('especialista', None)
        if start_date is None and end_date is None:
            start_date = datetime.today()
            end_date = datetime.today() + timedelta(days=1)

        eventos = Cita.objects.filter(fecha_inicio__gte=start_date,
                                      fecha_fin__lte=end_date).order_by('id')

        if medico is not None:
            eventos = eventos.filter(medico_id=medico)

        for evento in eventos:
            evento_dict = {
                'title': "{}".format(evento.titulo),
                'backgroundColor': evento.color,
                'start': str(evento.fecha_inicio),
                'end': str(evento.fecha_fin),
                'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data

            }
            response.append(evento_dict)

    except Cita.DoesNotExist:
        print("Cita does not exist")
        response = {'rc': 500,
                    'msg': 'Error loading Specialists', 'data': None}
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def seleccionar_tipo_cita(request, horario_id):
    request.session.pop('horario_cita', horario_id)
    return render(request, 'cita/seleccionar_tipo_cita.html')


@login_required
def calendario_registrar_cita(request):
    if request.user.groups.filter(name="terapeuta"):
        return redirect('/acceso-denegado/')

    if request.method == "POST":
        try:
            cita_id = request.POST.get('evento-cita')
            observaciones = request.POST.get('observaciones')
            paciente = request.POST.get('paciente')
            tipo_cita = request.POST.get('tipoCita')
            recuerrente_si = request.POST.get('eventoRecurrente')
            paciente = Paciente.objects.get(pk=paciente)
            cita = Cita.objects.get(pk=cita_id)
            recuerrente = True if recuerrente_si == "recurrente" else False

            request.session['fecha_evento_creado'] = cita.fecha_inicio.__str__()

            if not recuerrente:
                crear_cita_paciente(cita, paciente, tipo_cita,
                                    observaciones, recuerrente)
            else:
                dia_semana = cita.dia_semana  # 0->Mon, 1->Tuesday...6->Sunday
                posicion_dia = cita.posicion_turno  # 9:00->0, 10:00->1 ...21:00->11
                medico = cita.medico
                cita_id = cita.pk
                espacios_medico = Cita.objects.filter(
                    dia_semana=dia_semana, posicion_turno=posicion_dia, medico=medico, fecha_inicio__gte=cita.fecha_inicio)
                print("Dates to update {}".format(espacios_medico.count()))
                for espacio in espacios_medico:
                    crear_cita_paciente(espacio, paciente, tipo_cita,
                                        observaciones, recuerrente)

            print("Set fecha evento creado:".format(
                request.session.get('fecha_evento_creado', False)))
            return redirect('citas:seleccionar_horario')
        except Cita.DoesNotExist:
            messages.add_message(request=request, level=messages.ERROR,
                                 message="Algunas citas no se crearon. Valide que cada espacio tenga asignado un especialista")
        except Exception as e:
            print(e)
            messages.add_message(request=request, level=messages.ERROR,
                                 message="Error creando la cita.")

        return redirect('citas:seleccionar_horario')

    return HttpResponse("Acceso denegado")


def crear_cita_paciente(cita, paciente, tipo_cita_id, observaciones, recuerrente):
    if cita.paciente is not None:
        raise Exception("Ya hay una cita para este paciente en este espacio {}".format(
            cita.fecha_inicio))
    try:
        tipo_cita = TCita.objects.get(pk=tipo_cita_id)
        cita.titulo = "{}: {} {}".format(
            cita.medico.nombre, paciente.nombre, paciente.primer_apellido)
        cita.paciente = paciente
        cita.estado = ECita.objects.get(estado=ECita.RESERVADA)
        cita.tipo = tipo_cita
        cita.color = tipo_cita.color
        cita.observaciones = observaciones
        cita.recurrente = recuerrente
        cita.save()
    except Exception as e:
        print("Fallo crear cita")
        print(e)


@login_required
def detalle_cita(request, cita_id):
    try:
        cita = Cita.objects.get(pk=cita_id)
        serializer = CitaSerializer(cita)
        response = {'rc': 200, 'msg': 'Specialists', 'data': serializer.data}
    except Cita.DoesNotExist:
        print("Cita does not exist")
        response = {'rc': 500,
                    'msg': 'Error loading Specialists', 'data': None}

    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def primera_cita(request):
    return render(request, 'cita/primera_cita.html')


@login_required
def nueva_cita(request):
    form = CitaForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.estado = ECita.objects.get(estado=ECita.RESERVADA)
            cita.save()
            return redirect('citas:listado_citas')
    context = {
        'form': form
    }
    return render(request, 'cita/nueva_cita.html', context=context)


@login_required
def primera_nueva_cita(request):
    form = PrimeraCitaForm()
    paciente_form = PacienteForm()
    if request.method == 'POST':
        form = CitaForm(request.POST)
        paciente_form = PacienteForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.estado = ECita.objects.get(estado=ECita.RESERVADA)
            cita.save()
            return redirect('citas:listado_citas')
    context = {
        'cita_form': form,
        'paciente_form': paciente_form
    }
    return render(request, 'cita/primera_cita.html', context=context)


@login_required
def editar_cita(request, cita_id):
    if request.user.groups.filter(name="terapeuta") or request.user.groups.filter(name="recepcion"):
        return redirect('/acceso-denegado/')

    cita = get_object_or_404(Cita, pk=cita_id)
    form = CitaForm(instance=cita)
    msg = None
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save(False)
            cita.titulo = "{} {} {}".format(
                cita.medico.nombre, cita.paciente.nombre, cita.paciente.primer_apellido)
            cita.save()
            msg = "Cita actualizada con éxito"

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'cita/editar_cita.html', context=context)


@login_required
def migrar_color_evento(request):
    eventos = Event.objects.all()
    print("Found:{}".format(eventos.count()))
    for evento in eventos:
        print("Evento with cita? {}".format(evento.cita))
        if not evento.cita:
            evento.color = "#99ADC1"
            evento.save()
    return HttpResponse("Done")


@login_required
def migrar(request):
    citas = Cita.objects.all()
    for cita in citas:
        evento = cita.events.first()
        dia_semana = evento.dia_semana
        for i in range(1, 5):
            dias = 7 * i
            fecha_cita = cita.fecha + timedelta(days=dias)
            fecha_fin = evento.hora_fin + timedelta(days=dias)
            crear_cita_evento(fecha_cita, cita.medico, cita.paciente, cita.tipo_id, cita.observaciones, fecha_fin, True,
                              dia_semana)
    return HttpResponse("OK")


@login_required
def listado_citas(request):
    if request.user.groups.filter(name="terapeuta"):
        return redirect('/acceso-denegado/')
    citas = Cita.objects.all().order_by('-id')
    paginator = Paginator(citas, 25)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'citas': page_obj
    }
    return render(request, 'cita/listado_citas.html', context=context)
