from django import forms

from hic.cita.models import Cita


class PrimeraCitaForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Cita
        fields = ('observaciones',)


class CitaForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Cita
        fields = ('paciente', 'observaciones')
