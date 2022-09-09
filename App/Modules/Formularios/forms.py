from django.db.models import fields
from django.db.models.base import Model
from django.forms.widgets import Select, TextInput
from django import forms
from App.models import *
from django.forms import ModelForm
class formularioFacultades(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Facultad
        fields = '__all__'
class formularioCarreras(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Carrera
        fields = '__all__'
class formularioListaVerificaciones(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['idEstudiante'].widget.attrs['autofocus'] = True

    class Meta:
        model = ListaVerificacion
        fields = '__all__'
class formularioProyectos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['idCarrera'].widget.attrs['autofocus'] = True
    class Meta:
        model = Proyecto
        fields = '__all__'
class formularioEstudiantes(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = Usuarios
        fields = '__all__'
class formularioTutorias(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['idProyecto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tutoria
        fields = '__all__'

class formularioGrupoExperto(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = GrupoExperto
        fields = '__all__'
