from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioTutorias
from App.models import GrupoExperto, Proyecto, Tutoria
from django.http.response import JsonResponse

from django.urls import reverse_lazy
modelo = Tutoria
formulario = formularioTutorias
entidad = 'Tutorias'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')
class listarTutorias(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombre = ''
        for grupo in GrupoExperto.objects.all():
            for user in grupo.idDocentes.all():
                if self.request.user == user:
                    nombre += f'<li><h5><b><i>{grupo.pk}</i></b></h5></li>'
        if nombre:
            nombre = f'<ul>{nombre}</ul>'
        context['grupo'] = nombre
        context['encabezado'] = ['#', 'proyecto', 'estudiante/s', 'fecha', 'Descripción de tutoría']
        context['title'] = f'{entidad}' 
        context['listado'] = f'Listado de {entidad}' 
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            admin = True if request.user.perfil.nombre == 'Admin' else False
            query = modelo.objects.all() if admin else modelo.objects.filter(idProyecto__idDocente = request.user.pk)
            for i in query:
                if admin:
                    data.append([
                        cont,
                        i.idProyecto.nombre,
                        i.idProyecto.getEstudiantes(),
                        i.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                        i.descripcion,
                        i.idProyecto.getDocente().getInformacion(),
                        None
                    ])
                else:
                    data.append([
                        cont,
                        i.idProyecto.nombre,
                        i.idProyecto.getEstudiantes(),
                        i.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                        i.descripcion,
                        i.id
                    ])
                cont +=1
        except Exception as e:
            print(f'Error al cargar los datos l-55 de {entidad}: ',e)
            data = {}
        return JsonResponse(data, safe=False)

    
class addTutorias(LoginRequiredMixin, CreateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['tutorias'] = f'{entidad}'
        context['idProyecto'] = Proyecto.objects.filter(idDocente = self.request.user.pk)
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        return context
class editTutorias(LoginRequiredMixin, UpdateView):
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
        context['tutorias'] = Tutoria.objects.get(id = self.kwargs['pk'])
        context['accion'] = f'Edición de {entidad}'
        return context
class deleteTutorias(LoginRequiredMixin, DeleteView):
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
