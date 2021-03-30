from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit
from django import forms
from hic.main.models import Paciente, Medico, Especialidad, Consultorio, Direccion, NEstado
from hic.paciente.models import HistoriaClinica
from crispy_forms.helper import FormHelper


class HistoriaClinicaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            HTML(
                """
                <h3>Datos generales</h3>
                                <hr>

                """
            ),
            Div(
                'fecha',
                'folio',
                'nombre_madre',
                'ocupacion_madre',
                'telefono_madre',
                'nombre_padre',
                'ocupacion_padre',
                'telefono_padre',
                'estado_civil',
                'escolaridad_menor',
                'nombre_colegio',
                'grado_cursa',
                'remitido_por',
                'servicio_solicitado',
                css_class='form-flex'
            ),
            Div(
                'diagnostico_medico',
                'motivo_consulta',
                'observaciones_generales',
                css_class='form-flex'
            ),
            HTML(
                """
                <h3>Datos administrativos</h3>
                <hr>
                """
            ),
            Div(
                'terapia_fisica',
                'terapia_ocupacional',
                'psicologia',
                'neuropsicologia',
                'psicopedagogia',
                'terapia_lenguaje',
                'neuroterapia',
                'estado',
                css_class='form-flex-sm'
            ),
            Div(
                'fecha_cita',
                'profesional_cargo',
                'costo_valoracion',
                'costo_terapias',
                'nombre_entrevistador',
                css_class='form-flex'
            ),
            Submit('Guardar', 'Guardar')
        )
        self.helper.form_style = 'inline'

    class Meta:
        model = HistoriaClinica
        exclude = ('paciente',)


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        exclude = ('usuario',)


class MedicoForm(forms.ModelForm):
    # CHOICES = [[x.id, x.nombre] for x in Especialidad.objects.all()]
    # especialidades = forms.MultipleChoiceField(choices=CHOICES, required=True, widget=forms.SelectMultiple)
    class Meta:
        model = Medico
        fields = '__all__'


class ConsultorioForm(forms.ModelForm):
    class Meta:
        model = Consultorio
        exclude = ('medico', 'direccion',)


class DireccionForm(forms.ModelForm):
    estado = forms.ModelChoiceField(queryset=NEstado.objects.filter(activo=True), empty_label='--selecciona--',
                                    label='Estado',
                                    required=False)

    class Meta:
        model = Direccion
        fields = '__all__'
