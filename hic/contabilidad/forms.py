from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit

from hic.contabilidad.models import Gasto

class GastoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
        Div(
            'fecha',
            'descripcion',
            'subcuenta',
            'entidad',
            'forma_pago',
            'recibo',
            'lugar',
            'factura',
            'total',
            css_class='form-flex'
        ),
        Submit('Guardar', 'Guardar')
        )

        self.helper.form_style = 'inline'

    class Meta:
        model= Gasto
        exclude =('fecha_registro',)