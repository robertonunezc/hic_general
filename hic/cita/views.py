from django.db.models.functions import datetime
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from hic import settings
from hic.cita.forms import CitaForm, PrimeraCitaForm
from hic.cita.models import Cita, ECita, Event, TCita, Calendario, EventExtendedProp
from hic.cita.serializer import EventoSerializer, CitaSerializer, EventExtendedPropSerializer
from hic.main.models import Paciente, Medico, Especialidad
from hic.paciente.forms import PacienteForm
from django.utils.timezone import localtime
import json
import pytz


@login_required
def seleccionar_horario(request):
    pacientes = Paciente.objects.all()
    especialistas = Medico.objects.all()
    leyenda_especialidades = Especialidad.objects.all()
    # serializer.data['extendedProps'] = serializer.data['extended_props']
    context = {
        'pacientes': pacientes,
        'especialistas': especialistas,
        'leyenda_especialidades': leyenda_especialidades
    }
    print(context)
    return render(request, 'cita/seleccionar_horario.html', context=context)

@login_required
def borrar_cita(request, cita_id):
    if request.method == 'POST':
        try:
            cita = Cita.objects.get(pk=cita_id)
            cita.deshabilitado = True
            cita.save()
            for evento in cita.events.all():
                evento.deshabilitado = True
                evento.save()
            return HttpResponseRedirect('/citas/horario')
        except Cita.DoesNotExist:
            print("No existe")
        except Exception as e:
            print(e)
    return render(request,'cita/confirmacion_borrar.html')

def cargar_eventos(request):
    try:
        response = []
        eventos = Event.objects.filter(tipo=1, deshabilitado=0)  # TODO only load the current month

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

    except Cita.DoesNotExist:
        print("Cita does not exist")
        response = {'rc': 500, 'msg': 'Error loading Specialists', 'data': None}

    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def seleccionar_tipo_cita(request, horario_id):
    request.session.pop('horario_cita', horario_id)
    return render(request, 'cita/seleccionar_tipo_cita.html')


@login_required
def calendario_registrar_cita(request):
    if request.method == "POST":
        especialista_id = request.POST.get('especialista')
        observaciones = request.POST.get('observaciones')
        inicio = request.POST.get('fecha-inicio-cita')
        fin = request.POST.get('fecha-fin-cita')
        paciente = request.POST.get('paciente')
        recuerrente_si = request.POST.get('eventoRecurrente')
        print(recuerrente_si)
        medico = Medico.objects.get(pk=especialista_id)
        paciente = Paciente.objects.get(pk=paciente)
        recuerrente = True if recuerrente_si == "recurrente" else False
        dia_semana = datetime.datetime.strptime(inicio, "%Y-%m-%dT%H:%M:%S%z").date().weekday()
        if dia_semana == 6:
            dia_semana = 0
        else:
            dia_semana += 1
        try:
            cita = Cita()
            cita.medico = medico
            cita.paciente = paciente
            cita.estado = ECita.objects.get(estado=ECita.RESERVADA)
            cita.tipo = TCita.objects.get(tipo=TCita.INICIAL)
            cita.observaciones = observaciones
            cita.calendario = Calendario.objects.first()
            cita.fecha = inicio
            cita.save()
        except Exception as e:
            print(e)
            return redirect('citas:listado_citas')

        try:
            evento = Event()
            evento.cita = cita
            evento.medico = medico
            evento.hora_inicio = inicio
            evento.hora_fin = fin
            evento.tipo = 1
            evento.color = medico.especialidades.first().especialidad.color
            evento.calendario = Calendario.objects.first()
            evento.titulo = "{}-RES".format(paciente.nombre)
            evento.recurrente = recuerrente
            evento.dia_semana = dia_semana
            evento.save()
        except Exception as e:
            print(e)
            cita.delete()
            return redirect('citas:seleccionar_horario')

        try:
            extendedProp = EventExtendedProp()
            extendedProp.doctor = medico.pk
            extendedProp.evento = evento.pk
            extendedProp.cita = cita.pk
            extendedProp.save()
            evento.extendedProps = extendedProp
            evento.save()
        except Exception as e:
            print(e)
            cita.delete()
            evento.delete()
            return redirect('citas:seleccionar_horario')

        return redirect('citas:seleccionar_horario')

    return HttpResponse("Acceso denegado")


@login_required
def detalle_cita(request, cita_id):
    try:
        cita = Cita.objects.get(pk=cita_id)
        serializer = CitaSerializer(cita)
        response = {'rc': 200, 'msg': 'Specialists', 'data': serializer.data}
    except Cita.DoesNotExist:
        print("Cita does not exist")
        response = {'rc': 500, 'msg': 'Error loading Specialists', 'data': None}

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
    cita = get_object_or_404(Cita, pk=cita_id)
    form = CitaForm(instance=cita)
    msg = None
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            msg = "Cita actualizada con éxito"

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'cita/editar_cita.html', context=context)


@login_required
def listado_citas(request):
    citas = Cita.objects.all().order_by('-fecha')
    context = {
        'citas': citas
    }
    return render(request, 'cita/listado_citas.html', context=context)
