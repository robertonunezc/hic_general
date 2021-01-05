from rest_framework import serializers

from hic.main.models import Medico

# class EventExtendedPropSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EventExtendedProp
#         fields = '__all__'


class SpecialistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medico
        fields = '__all__'
        depth = 1
