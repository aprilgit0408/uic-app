from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioTutorias
from App.models import Proyecto, Tutoria
from django.http.response import JsonResponse
from App.funciones import send_mail, getDate
from django.template.loader import render_to_string

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
        context['encabezado'] = ['#', 'proyecto', 'estudiante/s', 'fecha', 'Descripción de tutoría'] if self.request.user.perfil.nombre != 'Estudiante' else ['#', 'proyecto', 'estudiantes','fecha', 'Descripción de tutoría']
        context['title'] = f'{entidad}' 
        context['listado'] = f'Listado de {entidad}' 
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            admin = True if request.user.perfil.nombre == 'Admin' else False
            estudiante = False
            query = modelo.objects.all() if admin else modelo.objects.filter(idProyecto__idDocente = request.user.pk)
            if request.user.perfil.nombre == 'Estudiante':
                query = modelo.objects.filter(idProyecto__idEstudiantes = request.user.pk)
                admin = False
                estudiante = True
            for i in query:
                if admin:
                    data.append([
                        cont,
                        i.idProyecto.nombre,
                        i.idProyecto.getEstudiantes(),
                        i.fechaTutoria.strftime("%Y-%m-%d %H:%M:%S"),
                        i.descripcion,
                        i.idProyecto.getDocente().getInformacion(),
                        None
                    ])
                else:
                    data.append([
                        cont,
                        i.idProyecto.nombre,
                        i.idProyecto.getEstudiantes(),
                        i.fechaTutoria.strftime("%Y-%m-%d %H:%M:%S"),
                        i.descripcion,
                        i.pk if not estudiante else None
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
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.cleaned_data['idProyecto']     
            descripcion = form.cleaned_data['descripcion']
            fechaEntrega = form.cleaned_data['fechaTutoria']
            emails = ''
            content = render_to_string('email.html',
                                       {'titulo': 'Avances', 
                                       'docente': self.request.user.getInformacion(), 
                                       'tema': 'solicitado una tutoría', 
                                       'proyecto': instance.nombre, 
                                       'requerimiento' : descripcion,
                                       'fechaEntrega' : getDate(fechaEntrega)
                                       })
            for i in instance.idEstudiantes.all():
                if emails:
                    emails += f',{i.email}'
                else:
                    emails = i.email
            send_mail('Tutoría', emails, content)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['tutorias'] = f'{entidad}'
        context['idProyectoTutoria'] = Proyecto.objects.filter(idDocente = self.request.user.pk)
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
            instance = form.cleaned_data['idProyecto']
            descripcion = form.cleaned_data['descripcion']
            fechaEntrega = form.cleaned_data['fechaTutoria']
            emails = ''
            content = render_to_string('email.html',
                                       {'titulo': 'Avances', 
                                       'docente': self.request.user.getInformacion(), 
                                       'tema': 'actualizado la tutoría', 
                                       'proyecto': instance.nombre, 
                                       'requerimiento' : descripcion,
                                       'fechaEntrega' : getDate(fechaEntrega)
                                       })
            for i in instance.idEstudiantes.all():
                if emails:
                    emails += f',{i.email}'
                else:
                    emails = i.email
            send_mail('Tutoría', emails, content)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['tutorias'] = Tutoria.objects.get(id = self.kwargs['pk'])
        context['accion'] = f'Edición de {entidad}'
        return context
class deleteTutorias(LoginRequiredMixin, DeleteView):
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
