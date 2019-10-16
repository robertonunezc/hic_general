from django import forms

from hic.consulta.models import Consulta


class ConsultaForm(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = '__all__'
