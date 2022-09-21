from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioFacultades
from Usuarios.models import Facultad 
from django.urls import reverse_lazy
from django.http.response import JsonResponse

modelo = Facultad
formulario = formularioFacultades
entidad = 'Facultades'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')
class listarFacultades(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#', 'nombre', 'sigla']
        context['items'] = modelo.objects.all()
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
                    i.sigla,
                    i.pk,
                ])
                cont +=1
        except Exception as e:
            print(f'Error al cargar los datos l-40 de {entidad}: ',e)
            data = {}
        return JsonResponse(data, safe=False)

    
class addFacultades(LoginRequiredMixin, CreateView):
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
class editFacultades(LoginRequiredMixin, UpdateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def post(self, request, *args, **kwargs):
        form = formulario(request.POST, instance=self.get_object())
        if form.is_valides():
            form.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Edición de {entidad}'
        return context
class deleteFacultades(LoginRequiredMixin, DeleteView):
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