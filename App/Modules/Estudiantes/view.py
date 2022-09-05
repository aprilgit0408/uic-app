from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.models import Usuarios
from django.urls import reverse_lazy
modelo = Usuarios
entidad = 'Estudiantes'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')
class listarEstudiantes(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['nombre', 'facultad']
        context['items'] = modelo.objects.filter()
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        return context
