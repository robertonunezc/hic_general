from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from hic.main.models import Paciente
from hic.paciente.forms import PacienteForm, HistoriaClinicaForm
from django.contrib.auth.decorators import login_required
from hic.pdf import get_historia_pdf
# Create your views here

@login_required
def listado_paciente(request):
    pacientes = Paciente.objects.all().order_by('-id')
    context = {
        'pacientes': pacientes
    }
    return render(request, 'pacientes/listado_pacientes.html', context=context)


@login_required
def nuevo_paciente(request):
    paciente_form = PacienteForm()
    historia_clinica_form = HistoriaClinicaForm()
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, request.FILES)
        if paciente_form.is_valid():
            historia_clinica_form = HistoriaClinicaForm(request.POST)
            if historia_clinica_form.is_valid():
                paciente = paciente_form.save()
                historia_clinica_form.instance.paciente = paciente
                historia_clinica_form.save()
                return redirect('pacientes:listado_pacientes')
    context = {
        'paciente_form': paciente_form,
        'historia_clinica_form': historia_clinica_form
    }
    return render(request, 'pacientes/alta_paciente.html', context=context)


@login_required
def editar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    form = PacienteForm(instance=paciente)
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes:listado_pacientes')
    context = {
        'form': form
    }
    return render(request, 'pacientes/editar_paciente.html', context=context)


@login_required
def historia_clinica(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    consultas = paciente.consultas.all().order_by('-id')
    historia_clinica = {
        'paciente': paciente,
        'consultas': consultas,
        'citas': paciente.citas.all()
    }
    context = {
        'historia_clinica': historia_clinica
    }
    return render(request, 'pacientes/historia_clinica.html', context=context)

@login_required
def ver_pdf_historia(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    consultas = paciente.consultas.all().order_by('-id')
    historia_clinica = {
        'paciente': paciente,
        'consultas': consultas,
        'citas': paciente.citas.all()
    }
    pdf = get_historia_pdf(historia_clinica)
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename=historia_clinica.pdf'
    response.write(pdf)
    return response