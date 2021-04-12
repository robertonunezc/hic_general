from django.contrib import admin

# Register your models here.
from hic.contabilidad.models import TipoPago, Gasto, LugarGasto, SubCuenta, TabuladorPrecios

admin.site.register(TipoPago)
admin.site.register(Gasto)
admin.site.register(SubCuenta)
admin.site.register(LugarGasto)
admin.site.register(TabuladorPrecios)
