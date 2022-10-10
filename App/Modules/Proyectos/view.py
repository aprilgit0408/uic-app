from django.views.generic import CreateView, ListView   
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioProyectos
from App.models import Proyecto
from Usuarios.models import Usuarios
from django.http.response import JsonResponse

from django.urls import reverse_lazy
modelo = Proyecto
formulario = formularioProyectos
entidad = 'Proyectos'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')
class listarProyectos(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        esEstudiante = True if self.request.user.perfil.nombre == 'Estudiante' else False
        context['encabezado'] = ['#', 'carrera','tema de investigación','estudiantes asignados'] if not esEstudiante else ['carrera','tema de investigación'] 
        context['title'] = f'{entidad}' 
        context['listado'] = f'Listado de {entidad}' 
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            admin = True if request.user.perfil.nombre == 'Admin' else False
            esEstudiante = True if request.user.perfil.nombre == 'Estudiante' else False
            query = modelo.objects.all() if admin else modelo.objects.filter(idDocente = request.user.pk)
            for i in query:
                if admin:
                    data.append([
                        cont,
                        i.idCarrera.nombre,
                        i.nombre,
                        i.getEstudiantes(),
                        i.getDocente().getInformacion(),
                        i.pk
                    ])
                elif esEstudiante:
                    data.append([
                        i.idCarrera.nombre,
                        i.nombre,
                        None
                    ])
                else:
                    data.append([
                        cont,
                        i.idCarrera.nombre,
                        i.nombre,
                        i.getEstudiantes(),
                        'Ver',
                        i.id
                    ])
                cont +=1
        except Exception as e:
            print(f'Error al cargar los datos l-60 de {entidad}: ',e)
            data = {}
        return JsonResponse(data, safe=False)

    
class addProyectos(LoginRequiredMixin, CreateView):
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
        context['idEstudiantes'] = Usuarios.objects.filter(perfil = 'Estudiante')
        return context
class editProyectos(LoginRequiredMixin, UpdateView):
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
        estudiantes = []
        listado = Proyecto.objects.get(id = self.kwargs['pk']).idEstudiantes.all()
        for i in Usuarios.objects.filter(perfil = 'Estudiante'):
            datosEst = {'pk' : i.pk, 'getInformacion' : i}
            if i in listado:
                datosEst['selected'] = True
                estudiantes.append(datosEst)
            elif self.request.user.perfil.nombre == 'Admin':
                datosEst['selected'] = False
                estudiantes.append(datosEst)
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Edición de {entidad}'
        context['idEstudiantes'] = estudiantes
        return context
class deleteProyectos(LoginRequiredMixin, DeleteView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def delete(self, request, *args, **kwargs):
        data = []
        id = int(self.kwargs['pk'])
        instance = modelo.objects.get(pk=id)
        instance.delete()
        return JsonResponse(data, safe=False)
        
class listarEstudiantes(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#', 'cédula', 'Nombre y Apellido', 'correo electrónico', 'teléfono', 'carrera', 'fotografía']
        context['title'] = 'Estudiantes'
        context['listado'] = f'Listado de Estudiantes'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            listadoEstudiantes = []
            admin = True if request.user.perfil.nombre == 'Admin' else False
            query = Usuarios.objects.filter(perfil = 'Estudiante') if admin else modelo.objects.filter(idDocente = request.user.pk)
            for item in query:
                if not admin:
                    for est in item.idEstudiantes.all():
                        if est not in listadoEstudiantes:
                            listadoEstudiantes.append(est)
                else:
                    listadoEstudiantes.append(item)

            for i in listadoEstudiantes:
                data.append([
                    cont,
                    i.username,
                    i.getInformacion(),
                    i.email,
                    i.celular,
                    i.idCarrera.nombre,
                    i.getImagen(),
                    False
                    ])
                cont +=1
        except Exception as e:
            print(f'Error al cargar los datos l-173 de {entidad}: ',e)
            data = {}
        return JsonResponse(data, safe=False)
class listarDocentes(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#', 'cédula', 'Nombre y Apellido', 'correo electrónico', 'teléfono', 'carrera', 'fotografía']
        context['title'] = 'Estudiantes'
        context['listado'] = f'Listado de Estudiantes'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            for i in Usuarios.objects.filter(perfil = 'Docente'):
                data.append([
                    cont,
                    i.username,
                    i.getInformacion(),
                    i.email,
                    i.celular,
                    i.idCarrera.nombre,
                    i.getImagen(),
                    False
                    ])
                cont +=1
        except Exception as e:
            print(f'Error al cargar los datos l-214 de {entidad}: ',e)
            data = {}
        return JsonResponse(data, safe=False)