"""
Formularios para el módulo personal.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
from .models import Area, SubArea, Personal, Roster


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'responsable', 'descripcion', 'activa']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn btn-primary'))


class SubAreaForm(forms.ModelForm):
    class Meta:
        model = SubArea
        fields = ['nombre', 'area', 'descripcion', 'activa']
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
            'cargo', 'tipo_trab', 'subarea', 'fecha_alta', 'fecha_cese', 'estado',
            'fecha_nacimiento', 'sexo', 'celular', 'correo_personal', 'correo_corporativo',
            'direccion', 'ubigeo', 'regimen_laboral', 'regimen_turno',
            'dias_libres_corte_2025', 'observaciones'
        ]
        widgets = {
            'fecha_alta': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_cese': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que las fechas se muestren en el formato correcto
        if self.instance and self.instance.pk:
            if self.instance.fecha_alta:
                self.initial['fecha_alta'] = self.instance.fecha_alta.strftime('%Y-%m-%d')
            if self.instance.fecha_cese:
                self.initial['fecha_cese'] = self.instance.fecha_cese.strftime('%Y-%m-%d')
            if self.instance.fecha_nacimiento:
                self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')
        
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
                    Column('subarea', css_class='col-md-6'),
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
