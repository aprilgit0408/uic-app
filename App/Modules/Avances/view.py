from django.views.generic.base import  View
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioAvances, formularioGuardarAvances
from App.models import Avance, Proyecto
from django.http.response import JsonResponse
from django.urls import reverse_lazy
modelo = Avance
formulario = formularioAvances
entidad = 'Avances'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')


class listarAvances(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#','Proyecto', 'nombre Avance', 'Estudiantes','observacion', 'porcentaje', 'archivo']
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
                    i.idProyecto.nombre,
                    i.nombreAvance,
                    i.idProyecto.getEstudiantes(),
                    f'<input type="text" name="observacion" class="form-control form-control-sm" id="idObservacion{i.pk}" value="{i.observacion if i.observacion else ""}" placeholder="Sin Observaciones" >',
                    f'<input type="number" style="width: 65px;" min="1" max="100" name="porcentaje" class="form-control form-control-sm" id="idPorcentaje{i.pk}" value="{i.porcentaje}" >',
                    'descargarArchivo',
                    'avances',
                    i.archivo.url if i.archivo else None,
                    i.pk

                ])
                cont +=1
        except Exception as e:
            print('Error Empleados l-43 ',e)
            data = {}
        return JsonResponse(data, safe=False)


class addAvances(LoginRequiredMixin, CreateView):
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
        context['idProyectoAvances'] = 'Avances'
        context['idProyectoAvancesList'] = Proyecto.objects.filter(idDocente = self.request.user.pk)
        return context


class editAvances(LoginRequiredMixin, UpdateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url

    def post(self, request, *args, **kwargs):
        form = formulario(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)
class guardarAvance(LoginRequiredMixin, View):
    template_name = main

    def post(self, request, *args, **kwargs):
        data = []
        try:
            id = int(request.POST['id'])
            observacion = request.POST['observacion']
            porcentaje = int(request.POST['porcentaje'])
            instance = Avance.objects.get(pk = id)
            instance.observacion = observacion
            instance.porcentaje = porcentaje
            instance.save()
            data.append({'info':'Datos Guardados'})
        except Exception as e:
            data.append({'info': str(e)})
            print('Error al guardar avances: ', e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Edición de {entidad}'
        return context


class deleteAvances(LoginRequiredMixin, DeleteView):
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
