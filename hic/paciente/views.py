from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from hic.paciente.forms import PacienteForm
from hic.main.models import Paciente, Consulta, Citas
from django.contrib.auth.decorators import login_required
from hic.pdf import get_historia_pdf
# Create your views here

@login_required
def listado(request):
    pacientes = Paciente.objects.all().order_by('-id')
    context = {
        'pacientes': pacientes
    }
    return render(request,'pacientes/listado_pacientes.html', context=context)


@login_required
def nuevo(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pacientes/listado')
    context = {
        'form': form
    }
    return render(request, 'pacientes/alta_paciente.html', context=context)


@login_required
def editar(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    form = PacienteForm(instance=paciente)
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/pacientes/listado')
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