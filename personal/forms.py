"""
Formularios para el módulo personal.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from .models import Gerencia, Area, Personal, Roster


class GerenciaForm(forms.ModelForm):
    class Meta:
        model = Gerencia
        fields = ['nombre', 'responsable', 'descripcion', 'activa']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-primary'))


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'gerencia', 'descripcion', 'activa']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-primary'))


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = [
            'tipo_doc', 'nro_doc', 'apellidos_nombres', 'codigo_fotocheck',
            'cargo', 'tipo_trab', 'area', 'fecha_alta', 'fecha_cese', 'estado',
            'fecha_nacimiento', 'sexo', 'celular', 'correo_personal', 'correo_corporativo',
            'direccion', 'ubigeo', 'afp', 'banco', 'cuenta_ahorros', 'cuenta_cci',
            'cuenta_cts', 'sueldo_base', 'bonos', 'regimen_laboral', 'regimen_turno',
            'dias_libres_corte_2025', 'observaciones'
        ]
        widgets = {
            'fecha_alta': forms.DateInput(attrs={'type': 'date'}),
            'fecha_cese': forms.DateInput(attrs={'type': 'date'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('tipo_doc', css_class='col-md-4'),
                    Column('nro_doc', css_class='col-md-4'),
                    Column('codigo_fotocheck', css_class='col-md-4'),
                ),
                Row(
                    Column('apellidos_nombres', css_class='col-md-12'),
                ),
                css_class='card mb-3 p-3'
            ),
            Div(
                Row(
                    Column('cargo', css_class='col-md-6'),
                    Column('tipo_trab', css_class='col-md-6'),
                ),
                Row(
                    Column('area', css_class='col-md-6'),
                    Column('estado', css_class='col-md-6'),
                ),
                Row(
                    Column('fecha_alta', css_class='col-md-6'),
                    Column('fecha_cese', css_class='col-md-6'),
                ),
                Row(
                    Column('regimen_laboral', css_class='col-md-6'),
                    Column('regimen_turno', css_class='col-md-6'),
                ),
                Row(
                    Column('dias_libres_corte_2025', css_class='col-md-12'),
                ),
                css_class='card mb-3 p-3'
            ),
            Submit('submit', 'Guardar', css_class='btn btn-primary')
        )


class RosterForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ['personal', 'fecha', 'codigo', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-primary'))


class ImportExcelForm(forms.Form):
    """Formulario para importación de archivos Excel."""
    archivo = forms.FileField(
        label='Archivo Excel',
        help_text='Selecciona un archivo .xlsx o .xls',
        widget=forms.FileInput(attrs={'accept': '.xlsx,.xls'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.add_input(Submit('submit', 'Importar', css_class='btn btn-primary'))
