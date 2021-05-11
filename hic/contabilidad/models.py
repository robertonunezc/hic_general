from django.db import models
from hic.main.models import Paciente

# Create your models here.

TIPOS_COBRO = (
    ('EVENTO', 'Por Evento'),
    ('TOTAL', 'Precio Total'),
)


class TipoPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class SubCuenta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class LugarGasto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Gasto(models.Model):
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    subcuenta = models.ForeignKey(
        SubCuenta, related_name='gastos', on_delete=models.PROTECT)
    entidad = models.CharField(max_length=250)
    forma_pago = models.ForeignKey(
        TipoPago, related_name='gastos', on_delete=models.PROTECT)
    recibo = models.CharField(max_length=250)
    lugar = models.ForeignKey(
        LugarGasto, related_name='gastos', on_delete=models.PROTECT)
    factura = models.CharField(max_length=250, null=True, blank=True)
    total = models.FloatField(default=0.0)
    fecha_registro = models.DateTimeField(auto_now=True)


class TabuladorPrecios(models.Model):
    nombre_servicio = models.CharField(max_length=50)
    precio = models.FloatField(default=0.0)
    tipo_cobro = models.CharField(
        choices=TIPOS_COBRO, default=TIPOS_COBRO[0], max_length=50)

    def __str__(self):
        return "{}- {}".format(self.nombre_servicio, self.precio)


class EstadoCuenta(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name='estado_cuenta')


class PacienteServicios(models.Model):
    servicio = models.ForeignKey(TabuladorPrecios, on_delete=models.PROTECT)
    estado_cuenta = models.ForeignKey(EstadoCuenta, on_delete=models.PROTECT)
    descuento = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
