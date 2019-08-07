from django import forms
from hic.main.models import Citas

class CitaForm(forms.ModelForm):

    class Meta:
        model = Citas
        fields = '__all__'
