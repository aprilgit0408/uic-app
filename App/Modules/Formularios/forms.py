from django.db.models import fields
from django.db.models.base import Model
from django.forms.widgets import Select, TextInput
from django import forms
from App.models import *
from django.forms import ModelForm
class formularioProyectos(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control form-control-sm'
            i.field.widget.attrs['autocomplete'] = 'off'
        # self.fields['idCarrera'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proyecto
        fields = '__all__'
