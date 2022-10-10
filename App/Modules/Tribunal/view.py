from cmath import log
from ctypes import Array
from pipes import Template
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioTribunal
from django.http.response import JsonResponse
from App.models import Tribunal
from django.urls import reverse_lazy

from Usuarios.models import GrupoExperto, Usuarios
modelo = Tribunal
formulario = formularioTribunal
entidad = 'Tribunal'
main = f'{entidad}/main.html'
url = reverse_lazy(f'app:{entidad.lower()}')


class listarTribunal(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#','nombre', 'facultad']
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            for i in modelo.objects.all():
                data.append([
                    cont,
                    i.nombre,
                    i.idFacultad.nombre,
                    i.pk
                ])
                cont +=1
        except Exception as e:
            print(f'Error {entidad} l-43 ',e)
            data = {}
        return JsonResponse(data, safe=False)


class addTribunal(LoginRequiredMixin, ListView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url

    def post(self, request, *args, **kwargs):
        data = []
        try:
            usuarios = request.POST['usuarios']
            usuarios = usuarios.split(',')
            for user in usuarios:
                if user:
                    data.append({'pk' : user, 'user' : Usuarios.objects.get(pk = int(user)).getInformacion()})
        except Exception as e:
            print('Error: ', e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docentes = Usuarios.objects.filter(perfil = 'Docente')
        data = []
        for user in docentes:
            data.append({'pk': user.pk, 'user': user, 'grupo' : user.getGrupoById(user)})
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        context['listadoDocentes'] = data
        return context


class editTribunal(LoginRequiredMixin, UpdateView):
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


class deleteTribunal(LoginRequiredMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        id = ''
        try:
            id = int(self.kwargs['pk'])
        except:
            id = str(self.kwargs['pk'])
        data = []
        instance = modelo.objects.get(pk=id)
        instance.delete()
        return JsonResponse(data, safe=False)
