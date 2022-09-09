from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioGrupoExperto
from App.models import GrupoExperto, Usuarios
from django.http.response import JsonResponse
from django.urls import reverse_lazy
modelo = GrupoExperto
formulario = formularioGrupoExperto
entidad = 'Grupo de Expertos'
main = 'main.html'
url = reverse_lazy('app:grupoExpertos')


class listarGrupoExpertos(LoginRequiredMixin, ListView):
    model = modelo
    template_name = 'GrupoExperto/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['nombre', 'Miembros']
        context['items'] = modelo.objects.all()
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        return context
   
class addGrupoExpertos(LoginRequiredMixin, CreateView):
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
        context['grupoExpertos'] = Usuarios.objects.filter(perfil = 'Docente')
        return context


class editGrupoExpertos(LoginRequiredMixin, UpdateView):
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
        context['grupoExpertos'] = Usuarios.objects.filter(perfil = 'Docente')
        return context


class deleteGrupoExpertos(LoginRequiredMixin, DeleteView):
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
