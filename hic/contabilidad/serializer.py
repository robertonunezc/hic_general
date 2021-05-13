from hic.contabilidad.models import TabuladorPrecios
from rest_framework import serializers


class TabuladorPrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabuladorPrecios
        fields = '__all__'
        depth = 1
