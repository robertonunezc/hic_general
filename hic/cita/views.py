from datetime import datetime, timedelta
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hic.cita.forms import CitaForm, PrimeraCitaForm
from hic.cita.models import Cita, ECita, Event, TCita, Calendario, EventExtendedProp
from hic.cita.serializer import EventoSerializer, CitaSerializer, EventExtendedPropSerializer
from hic.main.models import Paciente, Medico, Especialidad, RegistroIncidencias
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
        url_loadevents='/citas/cargar/eventos/?especialista={}'.format(medico)

    # I use this variable to move the calendar to specific date after an event was created
    if request.session.get('fecha_evento_creado', False):
        fecha_evento = request.session.get('fecha_evento_creado', False)


    context = {
        'pacientes': pacientes,
        'especialistas': especialistas,
        'tipo_citas': tipo_citas,
        'url_loadevents':url_loadevents,
        'fecha_evento':fecha_evento

    }
    print(context)
    return render(request, 'cita/seleccionar_horario.html', context=context)

@login_required
def borrar_cita(request, cita_id):
    if request.method == 'POST':
        try:
            motivo = request.POST.get("motivo")
            cita = Cita.objects.get(pk=cita_id)
            cita.deshabilitado = True
            cita.save()
            for evento in cita.events.all():
                evento.deshabilitado = True
                evento.save()
            incidencia = RegistroIncidencias()
            incidencia.accion = "Borrado cita {}".format(cita.pk)
            incidencia.comentario = motivo
            incidencia.usuario = request.user
            incidencia.save()
            return HttpResponseRedirect('/citas/horario')
        except Cita.DoesNotExist:
            print("No existe")
        except Exception as e:
            print(e)
    return render(request,'cita/confirmacion_borrar.html')

@login_required
def cargar_eventos(request):
    try:
        response = []
        medico = request.GET.get('especialista', None)
        if medico is not None:
            eventos =  Event.objects.filter(tipo=1, deshabilitado=0, medico_id=medico)
        else:
            eventos = Event.objects.filter(tipo=1, deshabilitado=0)  # TODO only load the current week and future

        for evento in eventos:
            cita_pagada = "PAGADA" if evento.cita.pagada else "APARTADA"
            evento_dict = {
                'title': "{} {} {}".format(evento.titulo, evento.cita.medico.nombre, cita_pagada),
                'backgroundColor': evento.color,
                'start': str(evento.hora_inicio),
                'end': str(evento.hora_fin),
                'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data

            }
            # if evento.recurrente:
            #     print(evento.hora_inicio.time())
            #     evento_dict = {
            #         'startRecur': datetime.strftime(evento.hora_inicio, '%Y-%m-%dT%H:%M:%S%z'),
            #         'daysOfWeek': [evento.dia_semana],
            #         'startTime': str(evento.hora_inicio.time()),
            #         'endTime': str(evento.hora_fin.time()),
            #         'title': evento.titulo,
            #         'backgroundColor': evento.color,
            #         'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data
            #     }
            # else:
            #     # TODO falta el cargar eventos sencillo
            #     evento_dict = {
            #         'title': evento.titulo,
            #         'backgroundColor': evento.color,
            #         'start': str(evento.hora_inicio),
            #         'end': str(evento.hora_fin),
            #         'extendedProps': EventExtendedPropSerializer(evento.extendedProps).data
            #
            #     }
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
        try:
            especialista_id = request.POST.get('especialista')
            observaciones = request.POST.get('observaciones')
            inicio = request.POST.get('fecha-inicio-cita')
            fin = request.POST.get('fecha-fin-cita')
            paciente = request.POST.get('paciente')
            tipo_cita = request.POST.get('tipoCita')
            recuerrente_si = request.POST.get('eventoRecurrente')
            cita_pagada_data = request.POST.get('eventoPagado')
            medico = Medico.objects.get(pk=especialista_id)
            paciente = Paciente.objects.get(pk=paciente)
            recuerrente = True if recuerrente_si == "recurrente" else False
            cita_pagada = True if cita_pagada_data == "pagada" else False
            cita_fecha = datetime.strptime(inicio, "%Y-%m-%dT%H:%M:%S")
            cita_fecha_fin =  datetime.strptime(fin, "%Y-%m-%dT%H:%M:%S")
            dia_semana = cita_fecha.date().weekday()
            if dia_semana == 6:
                dia_semana = 0
            else:
                dia_semana += 1

            if not recuerrente:
                crear_cita_evento(cita_fecha, medico, paciente, tipo_cita, observaciones, cita_fecha_fin, recuerrente,
                                  dia_semana, cita_pagada)
            else:
                print(cita_fecha_fin)
                for i in range(0,5):
                    print("crendo citas{}".format(i))
                    days = 7 * i
                    fecha_inicio = cita_fecha + timedelta(days=days)
                    fecha_fin = cita_fecha_fin + timedelta(days=days)
                    crear_cita_evento(fecha_inicio, medico, paciente, tipo_cita, observaciones, fecha_fin, recuerrente, dia_semana, cita_pagada)
            request.session['fecha_evento_creado'] = inicio
            return redirect('citas:seleccionar_horario')

        except Exception as e:
            print(e)
            messages.add_message(request=request,level=messages.ERROR,message="Error creando la cita. Todos los datos son obligatorios")
            return redirect('citas:seleccionar_horario')


    return HttpResponse("Acceso denegado")


def crear_cita_evento(cita_fecha,medico,paciente,tipo_cita_id, observaciones, fecha_fin, recurrente, dia_semana, cita_pagada):
    try:
        cita = Cita()
        cita.medico = medico
        cita.paciente = paciente
        cita.estado = ECita.objects.get(estado=ECita.RESERVADA)
        cita.tipo = TCita.objects.get(pk=tipo_cita_id)
        cita.observaciones = observaciones
        cita.calendario = Calendario.objects.first()
        cita.fecha = cita_fecha
        cita.fecha_fin = fecha_fin
        cita.pagada = cita_pagada
        cita.save()
        """SAVE EVENT"""
        evento = Event()
        evento.cita = cita
        evento.medico = medico
        evento.hora_inicio = cita_fecha
        evento.hora_fin = fecha_fin
        evento.tipo = 1
        evento.color = cita.tipo.color
        evento.calendario = Calendario.objects.first()
        evento.titulo = paciente.nombre
        evento.recurrente = recurrente
        evento.dia_semana = dia_semana
        evento.save()

        """SAVE EXTENDED PROP"""
        extendedProp = EventExtendedProp()
        extendedProp.doctor = medico.pk
        extendedProp.evento = evento.pk
        extendedProp.cita = cita.pk
        extendedProp.save()
        evento.extendedProps = extendedProp
        evento.save()
    except Exception as e:
        print(e)


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
            eventos = Event.objects.filter(cita=cita)
            for evento in eventos:
                evento.titulo = cita.paciente.nombre
                evento.hora_inicio = cita.fecha
                evento.hora_fin = cita.fecha_fin
                evento.dia_semana = cita.fecha.date().weekday()
                evento.medico = cita.medico
                evento.color = cita.tipo.color
                evento.save()
            msg = "Cita actualizada con éxito"

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, 'cita/editar_cita.html', context=context)


@login_required
def migrar(request):
    citas = Cita.objects.all()
    for cita in citas:
        evento = cita.events.first()
        dia_semana = evento.dia_semana
        for i in range(1,5):
            dias = 7 * i
            fecha_cita = cita.fecha + timedelta(days=dias)
            fecha_fin = evento.hora_fin + timedelta(days=dias)
            crear_cita_evento(fecha_cita,cita.medico,cita.paciente,cita.tipo_id, cita.observaciones, fecha_fin,True,dia_semana)
    return HttpResponse("OK")
@login_required
def listado_citas(request):
    citas = Cita.objects.all().order_by('-id')
    context = {
        'citas': citas
    }
    return render(request, 'cita/listado_citas.html', context=context)
