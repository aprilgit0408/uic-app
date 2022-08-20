from django.db import models
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django import forms
from App.Modules.Formularios.forms import formularioProyectos
from App.models import Proyecto
from django.urls import reverse_lazy
modelo = Proyecto
formulario = formularioProyectos
folder = 'Admin'
entidad = 'Proyectos'
main = 'main.html'
url = reverse_lazy('app:proyectos')
class listarProyectos(ListView):
    model = Proyecto
    template_name = f'{folder}/listado.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['carrera','nivel','nombre del proyecto','docente','estudiantes']
        context['items'] = Proyecto.objects.all()
        context['title'] = 'Proyectos' 
        context['listado'] = 'Listado de Proyectos' 
        return context
    
class addProyectos(CreateView):
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
class editProyectos(UpdateView):
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
        context['cancelar'] = "{% url 'app:proyectos' %}"
        return context
class deleteProyectos(DeleteView):
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