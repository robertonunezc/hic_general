from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
from hic.contabilidad.models import Gasto


@login_required
def listado_gastos(request):
    fecha_inicio = datetime.now().month
    # fecha_fin =
    gastos = Gasto.objects.all()
    context = {
        gastos
    }
    return render(request, 'gastos/listado_gastos.html', context=context)

@login_required
def nuevo_gasto(request):
    return ""

@login_required
def editar_gasto(request):
    return ""