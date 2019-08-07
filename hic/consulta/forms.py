from django import forms
from hic.main.models import Consulta

class ConsultaForm(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = '__all__'
