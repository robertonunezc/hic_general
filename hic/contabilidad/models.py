from django.db import models

# Create your models here.


class TipoPago(models.Model):
    nombre = models.CharField(max_length=50)


class SubCuenta(models.Model):
    nombre = models.CharField(max_length=50)

class LugarGasto(models.Model):
    nombre = models.CharField(max_length=50)

class Gasto(models.Model):
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    subcuenta = models.ForeignKey(SubCuenta, related_name='gastos', on_delete=models.PROTECT)
    entidad = models.CharField(max_length=250)
    forma_pago = models.ForeignKey(TipoPago, related_name='gastos', on_delete=models.PROTECT)
    recibo = models.CharField(max_length=250)
    lugar = models.ForeignKey(LugarGasto, related_name='gastos', on_delete=models.PROTECT)
    factura = models.CharField(max_length=250, null=True, blank=True)
    total = models.FloatField(default=0.0)
    fecha_registro = models.DateTimeField(auto_now=True)
