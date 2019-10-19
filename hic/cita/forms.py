from django import forms

from hic.cita.models import Cita


class CitaForm(forms.ModelForm):

    class Meta:
        model = Cita
        fields = ('fecha', 'paciente', 'tipo', 'calendario')
