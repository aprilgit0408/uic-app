from django.db import models
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django import forms
from App.Modules.Formularios.forms import formularioEstudiantes
from App.models import Estudiante
from django.urls import reverse_lazy
modelo = Estudiante
formulario = formularioEstudiantes
entidad = 'Estudiantes'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')
class listarEstudiantes(ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['carrera', 'nombre','apellido','e-mail','dirección','celular','fotografía']
        context['items'] = modelo.objects.all()
        context['title'] = f'{entidad}' 
        context['listado'] = f'Listado de {entidad}' 
        return context
    
class addEstudiantes(CreateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        return context
class editEstudiantes(UpdateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def post(self, request, *args, **kwargs):
        form = formulario(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Edición de {entidad}'
        return context
class deleteEstudiantes(DeleteView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Eliminar {entidad}'
        context['eliminar'] = kwargs
        return context