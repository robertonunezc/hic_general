from hic.main.models import Paciente
from django.http.response import HttpResponse
from hic.contabilidad.serializer import TabuladorPrecioSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
from hic.contabilidad.forms import GastoForm
from hic.contabilidad.models import EstadoCuenta, Gasto, PacienteServicios, TabuladorPrecios
from django.contrib import messages
import json


@login_required
def listado_gastos(request):
    if not request.user.is_superuser and not request.user.groups.filter(name="administrador"):
        return redirect('/acceso-denegado/')
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


def detalle_servicio(request, servicio_id):
    try:
        servicio = TabuladorPrecios.objects.get(pk=servicio_id)
        serializer = TabuladorPrecioSerializer(servicio)
        response = {'code': 200, 'data': serializer.data, 'msg': "OK"}
    except TabuladorPrecios.DoesNotExist:
        print("Servicio does not exist")
        response = {'code': 500,
                    'msg': 'Error loading servicio', 'data': None}
    return HttpResponse(json.dumps(response), content_type="application/json")


def agregar_servicio_paciente(request, servicio_id, paciente_id):
    try:
        servicio = TabuladorPrecios.objects.get(pk=servicio_id)
        paciente = Paciente.objects.get(pk=paciente_id)
        descuento = request.GET.get('discount', 0)
        "Create estado cuenta if not exist"
        estado_cuenta = EstadoCuenta.objects.filter(paciente=paciente)
        if not estado_cuenta.exists():
            estado_cuenta = EstadoCuenta()
            estado_cuenta.paciente = paciente
            estado_cuenta.save()
        else:
            estado_cuenta = estado_cuenta.first()

        "Find if the service exist in this estado_cuenta"
        paciente_servicios = PacienteServicios.objects.filter(
            servicio=servicio, estado_cuenta=estado_cuenta).exists()
        if not paciente_servicios:
            paciente_servicios = PacienteServicios()
            paciente_servicios.estado_cuenta = estado_cuenta
            paciente_servicios.servicio = servicio
            paciente_servicios.descuento = descuento
            paciente_servicios.total = servicio.precio
            # paciente_servicios.total = servicio.precio if int(
            #     descuento) > 0 else servicio.precio / (100+int(descuento))/100
            paciente_servicios.save()
        else:
            response = {'code': 500,
                        'msg': 'El servicio que está agregando ya existe', 'data': None}
            return HttpResponse(json.dumps(response), content_type="application/json")

        serializer = TabuladorPrecioSerializer(servicio)
        response = {'code': 200, 'data': serializer.data, 'msg': "OK"}

    except Exception as e:
        print(e)

        response = {'code': 500,
                    'msg': 'Error loading servicio', 'data': None}
    return HttpResponse(json.dumps(response), content_type="application/json")
