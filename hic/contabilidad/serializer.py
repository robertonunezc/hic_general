from hic.contabilidad.models import PacienteServicios, TabuladorPrecios
from rest_framework import serializers


class TabuladorPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabuladorPrecios
        fields = '__all__'
        depth = 1


class PacienteServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteServicios
        fields = '__all__'
        depth = 1
