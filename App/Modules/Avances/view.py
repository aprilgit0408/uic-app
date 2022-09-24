from django.views.generic.base import  View
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioAvances, formularioAvancesEstudiante
from App.models import Avance, Proyecto
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from Usuarios.models import Usuarios
from uicApp import settings
from django.template.loader import render_to_string
from App.sendMail import send_mail
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
        admin = True if self.request.user.perfil.nombre == 'Admin' else False
        carreras = []
        query = Proyecto.objects.all().order_by('idCarrera__nombre') if admin else Proyecto.objects.filter(idDocente = self.request.user.pk).order_by('idCarrera__nombre')
        for i in query:
            if i.idCarrera not in carreras:
                carreras.append(i.idCarrera)
        context['encabezado'] = ['#','carrera','Proyecto', 'nombre Avance', 'Estudiantes','Fecha entrega', 'observacion', 'porcentaje', 'opciones', 'estado']
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        context['idProyectos'] = query
        context['idCarreras'] = carreras
        return context
    def post(self, request, *args, **kwargs):
        idCarrera = request.POST['idCarrera']
        idProyecto = int(request.POST['idProyecto'])
        data = []
        try:
            cont = 1
            noEstudiante = True
            query = [] 
            if request.user.perfil.nombre == 'Admin':
                query = modelo.objects.all()
            elif request.user.perfil.nombre == 'Docente':
                query = modelo.objects.filter(idProyecto__idDocente = request.user.pk)
            else:
                noEstudiante = False
                for av in Avance.objects.all():
                    for est in av.idProyecto.idEstudiantes.all():
                        if est == request.user:
                            query.append(av)

            if(idCarrera != '0'):
                query = query.filter(idProyecto__idCarrera__nombre = idCarrera)
            if(idProyecto != 0):
                query = query.filter(idProyecto = idProyecto)
            for i in query:
                estado = 'checked disabled' if i.archivo else 'disabled'
                fecha = settings.getDate(i.fechaModificacion) if request.user.perfil.nombre == 'Estudiante' else ''
                svg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">   <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>   <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/> </svg>'
                descargar = f'<a type="button" href="{i.archivo.url}" title="Archivo subido el {settings.getDate(i.fechaModificacion)}, descargar" class="btn btn-success">{svg}</a> <i style="font-size: 13px;" title="Fecha de subida">{fecha}</i> ' if i.archivo else f'<button type="button" title="Sin Archivo" readonly class="btn btn-outline-secondary"  >{svg}</button>'
                guardarCambios = f'''
                    <div class="col-md">
                            <button type="submit" onClick="guardarAvances({i.pk})" class="btn btn-outline-warning" title="Guardar Cambios">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sd-card" viewBox="0 0 16 16">
                                <path d="M6.25 3.5a.75.75 0 0 0-1.5 0v2a.75.75 0 0 0 1.5 0v-2zm2 0a.75.75 0 0 0-1.5 0v2a.75.75 0 0 0 1.5 0v-2zm2 0a.75.75 0 0 0-1.5 0v2a.75.75 0 0 0 1.5 0v-2zm2 0a.75.75 0 0 0-1.5 0v2a.75.75 0 0 0 1.5 0v-2z"/>
                                <path fill-rule="evenodd" d="M5.914 0H12.5A1.5 1.5 0 0 1 14 1.5v13a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 14.5V3.914c0-.398.158-.78.44-1.06L4.853.439A1.5 1.5 0 0 1 5.914 0zM13 1.5a.5.5 0 0 0-.5-.5H5.914a.5.5 0 0 0-.353.146L3.146 3.561A.5.5 0 0 0 3 3.914V14.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-13z"/>
                                </svg>
                            </button>
                        </div>
                        <div class="col-md">
                            <button type="button" onClick="eliminarRegistro({i.pk})" class="btn btn-outline-danger" title="Eliminar Registro" >
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bucket" viewBox="0 0 16 16">
                                <path d="M2.522 5H2a.5.5 0 0 0-.494.574l1.372 9.149A1.5 1.5 0 0 0 4.36 16h7.278a1.5 1.5 0 0 0 1.483-1.277l1.373-9.149A.5.5 0 0 0 14 5h-.522A5.5 5.5 0 0 0 2.522 5zm1.005 0a4.5 4.5 0 0 1 8.945 0H3.527zm9.892 1-1.286 8.574a.5.5 0 0 1-.494.426H4.36a.5.5 0 0 1-.494-.426L2.58 6h10.838z"/>
                                </svg>
                            </button>
                        </div>
                        <div class="col-md">
                            {descargar}
                        </div>
                '''
                if noEstudiante:
                    data.append([
                        cont,
                        i.idProyecto.idCarrera.nombre,
                        i.idProyecto.nombre,
                        i.nombreAvance,
                        i.idProyecto.getEstudiantes(),
                        settings.getDate(i.fechaEntrega),
                        f'<textarea name="observacion" class="form-control form-control-sm" id="idObservacion{i.pk}" cols="5" rows="5">{i.observacion if i.observacion else ""}</textarea>',
                        f'<input type="number" style="width: 65px;" min="0" max="100" name="porcentaje" class="form-control form-control-sm" id="idPorcentaje{i.pk}" value="{i.porcentaje}" >',
                        guardarCambios,
                        f'<div class="form-check form-switch"><input name="estado" {estado} class="form-check-input" type="checkbox" ></div>',
                        None
                    ])
                else:
                    data.append([
                        cont,
                        i.idProyecto.idCarrera.nombre,
                        i.idProyecto.nombre,
                        i.nombreAvance,
                        i.idProyecto.getEstudiantes(),
                        settings.getDate(i.fechaEntrega),
                        i.observacion,
                        f'{i.porcentaje} %',
                        f'''
                        <form action="guardar/{i.pk}" id="form" method="post" name="form" enctype="multipart/form-data">
                            <input type="file" style="width: 300px; overflow:hidden; white-space:nowrap;text-overflow: ellipsis;" required name="archivo" class="form-control" id="idArchivo">
                            <hr>
                            <button type="submit" class="btn btn-outline-primary" title="Subir Archivo">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-upload" viewBox="0 0 16 16">   
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                            <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
                            </svg>
                            </button>
                            {descargar}
                        </form>
                        ''',
                        f'<div class="form-check form-switch"><input name="estado" {estado} class="form-check-input" type="checkbox" ></div>',
                        None
                    ])

                cont +=1
        except Exception as e:
            print(f'Error {entidad} l-161: ',e)
            data = {}
        return JsonResponse(data, safe=False)


class addAvances(LoginRequiredMixin, CreateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.cleaned_data['idProyecto']
            nombreAvance = form.cleaned_data['nombreAvance']
            fechaEntrega = form.cleaned_data['fechaEntrega']
            emails = ''
            docente = Usuarios.objects.get(pk = instance.idDocente)
            content = render_to_string('email.html',
                                       {'titulo': 'Avances', 
                                       'docente': docente.getInformacion(), 
                                       'tema': 'un nuevo avance', 'proyecto':instance.nombre, 
                                       'requerimiento' : nombreAvance,
                                       'fechaEntrega' : settings.getDate(fechaEntrega)
                                       })
            for i in instance.idEstudiantes.all():
                if emails:
                    emails += f',{i.email}'
                else:
                    emails = i.email
            send_mail('Nuevo Avance', emails, content)
            form.save()
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


class guardarAvanceEstudiante(LoginRequiredMixin, UpdateView):
    model = modelo
    form_class = formularioAvancesEstudiante
    template_name = main
    success_url = url
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)



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
