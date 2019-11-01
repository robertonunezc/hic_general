from django import forms

from hic.cita.models import Cita, SHorarioConsulta


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


class SHorarioConsultaForm(forms.ModelForm):
    class Meta:
        model = SHorarioConsulta
        fields = '__all__'
