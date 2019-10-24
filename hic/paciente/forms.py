from django import forms
from hic.main.models import Paciente, Medico, Especialidad, Consultorio, Direccion


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'


class MedicoForm(forms.ModelForm):
    CHOICES = [[x.id, x.nombre] for x in Especialidad.objects.all()]

    especialidades = forms.MultipleChoiceField(choices=CHOICES, required=True, widget=forms.SelectMultiple)

    class Meta:
        model = Medico
        fields = '__all__'


class ConsultorioForm(forms.ModelForm):

    class Meta:
        model = Consultorio
        exclude = ('medico', 'direccion',)


class DireccionForm(forms.ModelForm):

    class Meta:
        model = Direccion
        fields = '__all__'
