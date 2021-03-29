from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
from hic.contabilidad.forms import GastoForm
from hic.contabilidad.models import Gasto
from django.contrib import messages


@login_required
def listado_gastos(request):
    fecha_inicio = datetime.now().month
    # fecha_fin =
    gastos = Gasto.objects.all()
    context = {
        'gastos': gastos
    }
    return render(request, 'gastos/listado_gastos.html', context=context)


@login_required
def nuevo_gasto(request):
    gasto_form = GastoForm()
    if request.method == "POST":
        gasto_form = GastoForm(request.POST)
        if gasto_form.is_valid():
            gasto_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Gasto guardado correctamente.')
            return redirect('contabilidad:listado_gastos')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error creando el gasto')

    context = {
        'gasto_form': gasto_form
    }
    return render(request, 'gastos/nuevo_gasto.html', context=context)


@login_required
def editar_gasto(request, gasto_id):
    return ""
