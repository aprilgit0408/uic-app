from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioArchivoListaVerificacion, formularioListaVerificaciones
from App.models import ListaVerificacion, NombreArchivoListaVerificacion, Proyecto
from django.urls import reverse_lazy
from App.funciones import send_mail, getDate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse

import datetime
modelo = ListaVerificacion
formulario = formularioListaVerificaciones
entidad = 'Lista de Verificación'
main = 'main.html'
url = reverse_lazy('app:listaVerificaciones')


class listarListaVerificaciones(LoginRequiredMixin, ListView):
    model = modelo
    template_name = 'Verificacion/listado.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admin = True if self.request.user.perfil.nombre == 'Admin' else False
        carreras = []
        query = Proyecto.objects.all().order_by('idCarrera__nombre') if admin else Proyecto.objects.filter(idDocente = self.request.user.pk).order_by('idCarrera__nombre')
        estudiante = []
        if self.request.user.perfil.nombre == 'Estudiante':
            for av in modelo.objects.filter(archivo = ''):
                    for est in av.idProyecto.idEstudiantes.all():
                        if est == self.request.user:
                            estudiante.append(av)
        for i in query:
            if i.idCarrera not in carreras:
                carreras.append(i.idCarrera)
        context['idProyectos'] = query
        context['idCarreras'] = carreras
        context['encabezado'] = ['#','Nombre','estado','archivo']
        context['items'] = modelo.objects.all()
        context['title'] = f'listaVerificacion'
        context['listado'] = f'{entidad}'
        context['nombreListaVerificacion'] = NombreArchivoListaVerificacion.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            id = request.POST['id']
            estado = request.POST['estado']
            instance = modelo.objects.get(pk = id)
            instance.estado = True if estado else False
            instance.save()
        except:
            pass
        try:
            idCarrera = request.POST['idCarrera']
            idProyecto = int(request.POST['idProyecto'])
            query = modelo.objects.all()
            if(idCarrera != '0'):
                query = query.filter(idProyecto__idCarrera__nombre = idCarrera)
            if(idProyecto != 0):
                query = query.filter(idProyecto = idProyecto)
            cont = 1
            for i in query:
                fecha = getDate(i.fechaModificacion) if request.user.perfil.nombre == 'Estudiante' else ''
                svg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">   <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>   <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/> </svg>'
                descargar = f'<a type="button" href="{i.archivo.url}" title="Archivo subido el {getDate(i.fechaModificacion)}, descargar" class="btn btn-success">{svg}</a> <i style="font-size: 13px;" title="Fecha de subida">{fecha}</i> ' if i.archivo else f'<button type="button" title="Sin Archivo" readonly class="btn btn-outline-secondary"  >{svg}</button>'
                data.append([
                    cont,
                    i.nombre.nombre,
                    f'<div class="form-check form-switch"><input onClick="guardarListaVerificacion({i.pk})" name="{i.pk}" { "checked" if i.estado else ""} class="form-check-input" type="checkbox" {f"id=guardarSolicitud{i.pk}" if self.request.user.perfil.nombre != "Estudiante" else "disabled"}></div>',
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
                        ''' if self.request.user.perfil.nombre == 'Estudiante' else f'<a href="{i.archivo.url}" >Descargar</a>' if i.archivo else '-',
                    None if self.request.user.perfil.nombre == 'Estudiante' else i.pk
                ])
                cont +=1
        except Exception as e:
            print(f'Error {entidad} l-43 ',e)
            data = {}
        return JsonResponse(data, safe=False)

class addListaVerificaciones(LoginRequiredMixin, CreateView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        items = []
        nombresListaV = []
        for i in modelo.objects.filter(idProyecto__idEstudiantes = self.request.user):
            nombresListaV.append(i.nombre)
        for item in NombreArchivoListaVerificacion.objects.all():
            if item not in nombresListaV:
                items.append(item)
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        context['listadoNombresVerificacion'] = items
        context['editarObser'] = 'Editar' if self.request.user.perfil.nombre != 'Estudiante' else None
        context['listaVerificacion'] = f'{entidad}'
        context['listaVerificacionAdd'] = f'{entidad}'
        context['listaVerificacionList'] = Proyecto.objects.filter(idEstudiantes = self.request.user).first()
        
        return context


class editListaVerificaciones(LoginRequiredMixin, UpdateView):
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
        context['cumplimiento'] = f'{entidad}'
        context['editarValor'] = datetime.datetime.now()
        context['listaVerificacion'] = f'{entidad}'
        context['editarObser'] = 'Editar' if self.request.user.perfil.nombre != 'Estudiante' else None
        context['listaVerificacionList'] = Proyecto.objects.filter(idEstudiantes = self.request.user).first()
        
        return context


class deleteListaVerificaciones(LoginRequiredMixin, DeleteView):
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

class guardarListaVerificacion(LoginRequiredMixin, UpdateView):
    model = modelo
    form_class = formularioArchivoListaVerificacion
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
