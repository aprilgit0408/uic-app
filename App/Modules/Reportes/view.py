from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from App.funciones import getDate, getMeses, idsListaVerificacionObl
from App.models import Proyecto, Tutoria, ListaVerificacion
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import datetime

from Usuarios.models import Carrera, Cohorte, Usuarios

modelo = Tutoria
entidad = 'Reportes'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')


class getReportes(LoginRequiredMixin, ListView):
    model = Tutoria
    template_name = f'{entidad}/listado.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def GraficoTutorias(self, idProyecto):
        data = []
        year = datetime.datetime.now().year
        general = []
        drilldown = []
        try:
            for i in range(1, 13):
                s = 0
                detalles = []
                for j in Tutoria.objects.filter(idProyecto = idProyecto, fechaTutoria__year = year, fechaTutoria__month__gte = i, fechaTutoria__month__lt = (i + 1)):
                    s += 1
                    detalles.append([f'{j.descripcion}, {getDate(j.fechaTutoria)}' , 100])
                general.append({'name' :getMeses(i-1), 'y' : s, 'drilldown': getMeses(i-1)})
                drilldown.append({'name' :getMeses(i-1), 'id' : getMeses(i-1), 'data': detalles})
            data= {'data': general, 'drilldown': drilldown}
        except Exception as e:
            print('Error: ', e)
        return data
    def GraficoDefensa(self):
        data = []
        year = datetime.datetime.now().year
        general = []
        drilldown = []
        try:
            for i in Carrera.objects.all():
                s = 0
                detalles = []
                for j in Proyecto.objects.filter(idCarrera = i.id):
                    s += 1
                    detalles.append([f'{j.nombre}- > {j.getEstudiantes()}' , 100])
                general.append({'name' :i.nombre, 'y' : s, 'drilldown': i.nombre})
                drilldown.append({'name' :i.nombre, 'id' : i.nombre, 'data': detalles})
            data= {'data': general, 'drilldown': drilldown}
        except Exception as e:
            print('Error: ', e)
        return data
    def GraficoCohorte(self):
        data = []
        general = []
        drilldown = []
        try:
            for i in Cohorte.objects.all():
                s = 0
                detalles = []
                for j in Usuarios.objects.filter(perfil__id = 3, cohorte = i):
                    s += 1
                    detalles.append([f'{j.idCarrera.nombre} > {j.getInformacion()}' , 100])
                general.append({'name' :i.cohorte, 'y' : s, 'drilldown': i.cohorte})
                drilldown.append({'name' :i.cohorte, 'id' : i.cohorte, 'data': detalles})
            data= {'data': general, 'drilldown': drilldown}
        except Exception as e:
            print('Error: ', e)
        return data
    def AprobacionEstudiantes(self):
        data = []
        general = []
        drilldown = []
        detallesAPR = []
        detallesNOP = []
        aprobados = 'Estudiantes Aprobados'
        noAprobados = 'Estudiantes no Aprobados'
        try:
            for user in Usuarios.objects.filter(perfil__id = 3):
                reqCompletos = ListaVerificacion.objects.filter(nombre__id__in = idsListaVerificacionObl(), idEstudiante = user, estado = True)
                if len(reqCompletos) == len(idsListaVerificacionObl()):
                   detallesAPR.append([f'{user.getInformacion()}' , len(reqCompletos)])
                else:
                   detallesNOP.append([f'{user.getInformacion()}' , len(reqCompletos)])
            general.append({'name' :aprobados, 'y' : len(detallesAPR), 'drilldown': aprobados})
            general.append({'name' :noAprobados, 'y' : len(detallesNOP), 'drilldown': noAprobados})
            drilldown.append({'name' :aprobados, 'id' : aprobados, 'data': detallesAPR})
            drilldown.append({'name' :noAprobados, 'id' : noAprobados, 'data': detallesNOP})
            data= {'data': general, 'drilldown': drilldown}
        except Exception as e:
            print('Error: ', e)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#','nombre', 'facultad']
        context['title'] = f'reportes'
        context['encabezado'] = ['Tutorias', 'Defensa', 'Cohorte', 'Aprobación Proceso']
        context['listado'] = f'Reportes'
        context['idProyectos'] = Proyecto.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            tipo = self.request.POST['tipo']
            idProyecto = self.request.POST['idProyecto']
            if tipo == 'Tutorias':
                data = self.GraficoTutorias(idProyecto)
            if tipo == 'Defensa':
                data = self.GraficoDefensa()
            if tipo == 'Cohorte':
                data = self.GraficoCohorte()
            if tipo == 'Aprobacion':
                data = self.AprobacionEstudiantes()
        except Exception as e:
            print(f'Error {entidad} l-43 ',e)
            data = {}
        return JsonResponse(data, safe=False)
