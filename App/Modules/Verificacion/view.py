from django.db import models
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django import forms
from App.Modules.Formularios.forms import formularioListaVerificaciones
from App.models import ListaVerificacion
from django.urls import reverse_lazy
import datetime
modelo = ListaVerificacion
formulario = formularioListaVerificaciones
entidad = 'Lista de Verificación'
main = 'main.html'
url = reverse_lazy('app:listaVerificaciones')


class listarListaVerificaciones(ListView):
    model = modelo
    template_name = 'Verificacion/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['estudiantes','observacion','cumplimiento','archivo']
        context['items'] = modelo.objects.all()
        context['title'] = f'{entidad}'
        context['listado'] = f'{entidad}'
        return context


class addListaVerificaciones(CreateView):
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
        context['cumplimiento'] = f'{entidad}'
        
        return context


class editListaVerificaciones(UpdateView):
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
        context['cumplimiento'] = f'{entidad}'
        context['editarValor'] = datetime.datetime.now()
        
        return context


class deleteListaVerificaciones(DeleteView):
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
