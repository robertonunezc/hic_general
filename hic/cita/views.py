from datetime import datetime, timedelta
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hic.cita.forms import CitaForm, PrimeraCitaForm
from hic.cita.models import Cita, ECita, Event, TCita, Calendario, EventExtendedProp
from hic.cita.serializer import EventoSerializer, CitaSerializer, EventExtendedPropSerializer
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
        url_loadevents = '/citas/cargar/eventos/?especialista={}'.format(medico)

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
    print(context)
    request.session['fecha_evento_creado'] = None
    return render(request, 'cita/seleccionar_horario.html', context=context)


@login_required
def borrar_cita(request, cita_id):
    if request.user.groups.filter(name="especialistas") or request.user.groups.filter(name="asistente"):
        return redirect('/acceso-denegado/')

    cita = Cita.objects.get(pk=cita_id)
    evento = cita.events.first()
    fecha = evento.hora_inicio.date()

    dia_semana = get_dia_semana(fecha.weekday())
    mes = get_mes(fecha.month)

    if request.method == 'POST':
        recuerrente_si = request.POST.get('eventoRecurrente')
        motivo = request.POST.get("motivo")
        borrado_recuerrente = True if recuerrente_si == "si-recurrente" else False
        print("Evento recurrente {}".format(recuerrente_si))
        try:
            # Borrado recurrente
            if borrado_recuerrente:
                start_time = datetime.strptime(str(cita.fecha), "%Y-%m-%d %H:%M:%S")
                for i in range(0, 52):
                    if i == 0:
                        cita_borrar = cita
                    else:
                        days = 7 * i
                        print("Itercion")
                        print(days)
                        new_start_time = start_time + timedelta(days=days)
                        print("Fecha a borrar: {}".format(new_start_time))
                        cita_borrar = Cita.objects.filter(fecha=new_start_time).first()

                    print("Cita a borrar: {}".format(cita_borrar))
                    if cita_borrar:
                        delete_date(cita_borrar=cita_borrar, motivo=motivo, usuario=request.user)
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
    context = {'cita': cita, 'dia_semana': dia_semana, 'mes': mes}

    return render(request, 'cita/confirmacion_borrar.html', context=context)


def delete_date(cita_borrar, motivo, usuario):
    try:

        for evento in cita_borrar.events.all():
            print("Evento a borrar: {}".format(evento.pk))
            evento.titulo = evento.medico.nombre
            evento.cita = None
            evento.color = "#99ADC1"
            evento.save()
        extendedProps = EventExtendedProp.objects.filter(cita=cita_borrar.pk)

        for extended in extendedProps:
            extended.cita = None
            extended.save()

        incidencia = RegistroIncidencias()
        incidencia.accion = "Borrado cita {}".format(cita_borrar.pk)
        incidencia.comentario = motivo
        incidencia.usuario = usuario
        incidencia.save()

        cita_borrar.delete()
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

        eventos = Event.objects.filter(tipo=0, deshabilitado=0, hora_inicio__gte=start_date,
                                       hora_fin__lte=end_date).order_by('id')

        if medico is not None:
            eventos = eventos.filter(medico_id=medico)

        for evento in eventos:
            cita_pagada = ""
            if evento.cita:
                cita_pagada = "PAGADA" if evento.cita.pagada else "APARTADA"

            evento_dict = {
                'title': "{} {}".format(evento.titulo, cita_pagada),
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
    if request.user.groups.filter(name="especialistas"):
        return redirect('/acceso-denegado/')

    if request.method == "POST":
        try:
            especialista_id = request.POST.get('especialista')
            evento_id = request.POST.get('evento-cita')
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
            cita_pagada = True if cita_pagada_data == "pagado" else False
            cita_fecha = datetime.strptime(inicio, "%Y-%m-%dT%H:%M:%S")
            cita_fecha_fin = datetime.strptime(fin, "%Y-%m-%dT%H:%M:%S")
            dia_semana = cita_fecha.date().weekday()

            request.session['fecha_evento_creado'] = inicio

            if dia_semana == 6:
                dia_semana = 0
            else:
                dia_semana += 1

            if not recuerrente:
                evento = Event.objects.get(pk=evento_id)
                crear_cita_evento(cita_fecha, medico, paciente, tipo_cita, observaciones, cita_fecha_fin, recuerrente,
                                  dia_semana, cita_pagada, evento)
            else:
                print(cita_fecha_fin)
                for i in range(0, 52):
                    print("crendo citas{}".format(i))
                    days = 7 * i
                    fecha_inicio = cita_fecha + timedelta(days=days)
                    fecha_fin = cita_fecha_fin + timedelta(days=days)
                    evento = Event.objects.get(hora_inicio=fecha_inicio, hora_fin=fecha_fin, medico=medico)
                    print("EVETBTI")
                    print(evento)
                    crear_cita_evento(fecha_inicio, medico, paciente, tipo_cita, observaciones, fecha_fin, recuerrente,
                                      dia_semana, cita_pagada, evento)
            print("Set fecha evento creado:".format(request.session.get('fecha_evento_creado', False)))
            return redirect('citas:seleccionar_horario')
        except Event.DoesNotExist:
            messages.add_message(request=request, level=messages.ERROR,
                                 message="Algunas citas no se crearon. Valide que cada espacio tenga asignado un especialista")
        except Exception as e:
            print(e)
            messages.add_message(request=request, level=messages.ERROR,
                                 message="Error creando la cita. Todos los datos son obligatorios")

        return redirect('citas:seleccionar_horario')

    return HttpResponse("Acceso denegado")


def crear_cita_evento(cita_fecha, medico, paciente, tipo_cita_id, observaciones, fecha_fin, recurrente, dia_semana,
                      cita_pagada, evento):
    cita = None
    print(tipo_cita_id)
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
    except Exception as e:
        print("Fallo crear cita")
        print(e)
    try:
        """FIND EVENT"""
        # evento = Event.objects.get(pk=evento_id)
        evento.cita = cita
        evento.color = cita.tipo.color
        evento.titulo = "{} {}".format(evento.medico.nombre, cita.paciente.nombre)
        evento.recurrente = recurrente
        evento.dia_semana = dia_semana
        evento.save()
    except Exception as e:
        print(e)
        print("Fallo crear evento")
    try:
        """SAVE EXTENDED PROP"""
        extendedProps = EventExtendedProp.objects.filter(evento=evento.pk)
        for prop in extendedProps:
            prop.cita = cita.pk
            prop.save()
    except Exception as e:
        print(e)
        print("Fallo crear extenden prop")


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
    if request.user.groups.filter(name="especialistas"):
        return redirect('/acceso-denegado/')

    cita = get_object_or_404(Cita, pk=cita_id)
    form = CitaForm(instance=cita)
    msg = None
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            eventos = Event.objects.filter(cita=cita)
            for evento in eventos:
                evento.titulo = "{} {}".format(cita.medico.nombre, cita.paciente.nombre)
                # evento.hora_inicio = cita.fecha
                # evento.hora_fin = cita.fecha_fin
                # evento.dia_semana = cita.fecha.date().weekday()
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
    citas = Cita.objects.all().order_by('-id')
    context = {
        'citas': citas
    }
    return render(request, 'cita/listado_citas.html', context=context)
