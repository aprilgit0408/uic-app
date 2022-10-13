from datetime import datetime
import uuid
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioTribunal
from django.http.response import JsonResponse
from App.models import DocentesSuplente, Proyecto, Tribunal
from django.urls import reverse_lazy
from backports.zoneinfo import ZoneInfo
from django.utils.dateparse import parse_datetime
from Usuarios.models import Constantes, Usuarios
from uicApp.settings import TIME_ZONE
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
                data.append({'pk' : user, 'user' : Usuarios.objects.get(pk = int(user)).getInformacion()})
        except Exception as e:
            print('Sin valor para usuario: ', e)
        
        try:
            idProyecto = request.POST['idProyecto']
            idDocentesPrincipales = request.POST['idDocentesPrincipales']
            idDocentesSuplentes = request.POST['idDocentesSuplentes']
            idAula = request.POST['idAula']
            idFecha = parse_datetime(request.POST['idFecha'])
            idFecha.replace(tzinfo=ZoneInfo(TIME_ZONE))
            uuID = str(uuid.uuid4())
            docSuplentes = DocentesSuplente.objects.create(uuID = uuID)
            DOC_SUP = []
            for ds in idDocentesSuplentes.split(','):
                DOC_SUP.append(Usuarios.objects.get(pk = int(ds)))
            docSuplentes.docentesSuplentes.set(DOC_SUP)
            docSuplentes.save()
            DOC_PRIN = []
            for ds in idDocentesPrincipales.split(','):
                DOC_PRIN.append(Usuarios.objects.get(pk = int(ds)))
            tribunal = Tribunal.objects.create(idProyecto = Proyecto.objects.get(pk = int(idProyecto)), docentesSuplentes = DocentesSuplente.objects.get(pk = uuID), fechaDefensa = idFecha, aula = idAula)
            tribunal.docentesPrincipales.set(DOC_PRIN)
            tribunal.save()
        except Exception as e:
            print('Sin valores a agregar: ', e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docentes = Usuarios.objects.filter(perfil = 'Docente')
        aulas = Constantes.objects.get(nombre = 'AULAS').valor
        data = []
        for user in docentes:
            data.append({'pk': user.pk, 'user': user, 'grupo' : user.getGrupoById(user)})
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        context['listadoDocentes'] = data
        context['AULAS'] = aulas.split(',')
        context['idProyectos'] = Proyecto.objects.all()
        context['DOC_PRIN'] = Constantes.objects.get(nombre = 'DOC_PRIN').valor
        context['DOC_SUP'] = Constantes.objects.get(nombre = 'DOC_SUP').valor
        context['DATE'] = datetime.now()

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
