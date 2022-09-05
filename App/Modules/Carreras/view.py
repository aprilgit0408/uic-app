from django.db import models
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioCarreras
from App.models import Carrera
from django.http.response import JsonResponse
from django.urls import reverse_lazy
modelo = Carrera
formulario = formularioCarreras
entidad = 'Carreras'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')


class listarCarreras(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['nombre', 'facultad']
        context['items'] = modelo.objects.all()
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            btn = ''
            for i in modelo.objects.all():
                data.append([
                    cont,
                    i.carrera,
                    i.nivel,
                    i.nombreCompleto(),
                    i.celular,
                    i.direccion, 
                    i.email,
                    btn
                ])
                cont +=1
        except Exception as e:
            print('Error Empleados l-54 ',e)
            data = {}
        return JsonResponse(data, safe=False)


class addCarreras(LoginRequiredMixin, CreateView):
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


class editCarreras(LoginRequiredMixin, UpdateView):
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


class deleteCarreras(LoginRequiredMixin, DeleteView):
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
