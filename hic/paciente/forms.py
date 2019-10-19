from django import forms
from hic.main.models import Paciente, Medico, TEspecialidad


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'


class MedicoForm(forms.ModelForm):
    CHOICES = [[x.id, x.nombre] for x in TEspecialidad.objects.all()]

    especialidades = forms.MultipleChoiceField(choices=CHOICES, required=True, widget=forms.SelectMultiple)

    class Meta:
        model = Medico
        fields = '__all__'
