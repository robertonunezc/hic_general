from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from hic.cita.forms import CitaForm, PrimeraCitaForm
from hic.cita.models import Cita, ECita, Event, TCita, Calendario, EventExtendedProp
from hic.cita.serializer import EventoSerializer
from hic.main.models import Paciente, Medico
from hic.paciente.forms import PacienteForm
import json
@login_required
def seleccionar_horario(request):
    eventos = Event.objects.filter(tipo=1) #TODO only load the current month
    serializer = EventoSerializer(eventos, many=True)
    pacientes = Paciente.objects.all()
    especialistas = Medico.objects.all()
    # serializer.data['extendedProps'] = serializer.data['extended_props']
    print(serializer.data)
    context = {
        'eventos': json.dumps(serializer.data),
        'pacientes': pacientes,
        'especialistas':especialistas
    }
    print(context)
    return render(request, 'cita/seleccionar_horario.html', context=context)


@login_required
def seleccionar_tipo_cita(request, horario_id):
    request.session.pop('horario_cita', horario_id)
    return render(request,'cita/seleccionar_tipo_cita.html')

@login_required
def calendario_registrar_cita(request):
    if request.method == "POST":
        doctor = request.POST.get('especialista')
        observaciones = request.POST.get('observaciones')
        inicio = request.POST.get('fecha-inicio-cita')
        fin = request.POST.get('fecha-fin-cita')
        paciente = request.POST.get('paciente')

        cita = Cita()
        cita.medico = Medico.objects.get(pk=doctor)
        cita.paciente = Paciente.objects.get(pk=paciente)
        cita.estado =  ECita.objects.get(estado=ECita.RESERVADA)
        cita.tipo = TCita.objects.get(tipo=TCita.INICIAL)
        cita.observaciones = observaciones
        cita.calendario = Calendario.objects.first()
        cita.fecha = inicio
        cita.save()

        evento = Event()
        evento.cita = cita
        evento.medico = cita.medico
        evento.hora_inicio = inicio
        evento.hora_fin = fin
        evento.tipo = 1
        evento.calendario = Calendario.objects.first()
        evento.titulo = "Cita-{}".format(cita.paciente.nombre)
        evento.save()

        return redirect('citas:listado_citas')

    return HttpResponse("Acceso denegado")

@login_required
def primera_cita(request):

    return render(request,'cita/primera_cita.html')

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
