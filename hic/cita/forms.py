from django import forms

from hic.cita.models import Cita, SHorarioConsulta


class CitaForm(forms.ModelForm):
    observaciones = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Cita
        fields = ('fecha', 'paciente', 'tipo', 'calendario', 'observaciones')


class SHorarioConsultaForm(forms.ModelForm):
    class Meta:
        model = SHorarioConsulta
        fields = '__all__'
