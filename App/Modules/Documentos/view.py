from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioDocumentos, formularioFirma
from django.views.generic.base import  View
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
import os
from django.core.files import File
from pathlib import Path
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from Usuarios.models import SeguimientoDocumentacion, Usuarios, Documento
from uicApp import settings
modelo = Documento
formulario = formularioDocumentos
formularioFirmaEst = formularioFirma
entidad = 'Documentos'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')


class listarDocumentos(LoginRequiredMixin, UpdateView):
    model = Usuarios
    template_name = f'{entidad}/listado.html'
    form_class = formularioFirmaEst
    success_url = url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    def get_object(self, queryset = None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encabezado'] = ['#','nombre del documento','estado' ,'archivo']
        context['items'] = Documento.objects.all()
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}'
        return context
    def getEstado(self, estado, cont, datosEstado):
        if estado == True:
            return 'Aprobado'
        if estado is None:
            return 'Rechazado'
        if estado == False and cont == 1 and len(datosEstado) == 0:
            return 'Enviar para iniciar proceso'
        if estado == False and cont > 1 and len(datosEstado) == 0:
            return 'Listo para enviar'
        if estado == False:
            return 'Pendiente por Aprobar'
        return 'Inhabilitado'
    def post(self, request, *args, **kwargs):
        try:
            nombre = request.POST['nombre']
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
            return super().post(request, *args, **kwargs)
        except Exception as e:
            pass
        data = []
        try:
            cont = 1
            getDocumentacionBKP = SeguimientoDocumentacion.objects.filter(idUsuario = request.user.pk)
            valorAnterior = ''
            for documentacion in Documento.objects.all():
                for perfil in documentacion.idPerfiles.all():
                    if perfil.nombre == 'Estudiante':
                        estado = [seguimiento for seguimiento in getDocumentacionBKP if seguimiento and seguimiento.idDocumento == documentacion]
                        habilitar = estado if estado else False
                        estadoPantalla = habilitar[0].estado if habilitar else  False if valorAnterior else False if cont == 1 else''
                        data.append([
                            cont,
                            documentacion.nombre,
                            self.getEstado(estadoPantalla, cont, estado),
                            'file',
                            estadoPantalla,
                            documentacion.archivo.url[-5:].split('.')[1],
                            documentacion.archivo.url,
                        ])
                        valorAnterior = habilitar[0].estado if habilitar else False
                cont +=1
        except Exception as e:
            print(f'Error {entidad} l-89 ',e)
            data = {}
        return JsonResponse(data, safe=False)

class addDocumentos(LoginRequiredMixin, CreateView):
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


class editDocumentos(LoginRequiredMixin, UpdateView):
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


class deleteDocumentos(LoginRequiredMixin, DeleteView):
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
class GuardarDocumento(LoginRequiredMixin, View):
    template_name = main
    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

    def generarPDFFirmado(self, nombreArchivo, request):
        pisa.showLogging()
        ruta = f'media/documentacion/{request.user.getInformacion()}-{nombreArchivo}.pdf'
        result_file = open(ruta, "w+b")
        usuario = Usuarios.objects.get(pk = request.user.pk)
        data = {
            'usuario': usuario,
            'fecha': datetime.datetime.now().date(),
            'encabezado' : f'{settings.STATIC_URL}images/encabezado.jpg',
            'imagenCentro' : f'{settings.STATIC_URL}images/imagenCentro.jpg',
            'piePagina' : f'{settings.STATIC_URL}images/piePagina.jpg'
        }
        template = get_template(f'{entidad}/{nombreArchivo}.html')
        html = template.render(data)
        #Guardar PDF
        pisa_status = pisa.CreatePDF(
        html, dest=result_file,
        link_callback=self.link_callback
        )
        return ruta
    def get(self, request, *args, **kwargs):
        idDocumento = Documento.objects.get(pk = self.kwargs['pk'])
        getRegistro = SeguimientoDocumentacion.objects.filter(idDocumento = idDocumento, idUsuario = request.user)
        if not getRegistro.exists():
            try:
                path = Path(self.generarPDFFirmado(idDocumento.nombre,request))
                with path.open(mode='rb') as f:
                    archivoCargado= File(f, name=path.name)
                    doc = SeguimientoDocumentacion.objects.create(idDocumento = idDocumento,idUsuario =  request.user, archivo = archivoCargado)
                    doc.save()
            except Exception as e:
                print('Error al guardar el archivo generado ln-202: ', e)
        else:
            #Actualizar Documento
            try:
                path = Path(self.generarPDFFirmado(idDocumento.nombre, request))
                with path.open(mode='rb') as f:
                    archivoCargado= File(f, name=path.name)
                    doc = getRegistro[0]
                    doc.archivo = archivoCargado
                    doc.save()
            except Exception as e:
                print('Error al Actualizar el archivo generado ln-213: ', e)

        return HttpResponseRedirect(url)
class generarPDF(LoginRequiredMixin, View):
    def link_callback(self, uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    def get(self, request, *args, **kwargs):
        pisa.showLogging()
        nombreArchivo = Documento.objects.get(pk = self.kwargs['pk']).nombre
        ruta = f'media/documentacion/{request.user.getInformacion()}-{nombreArchivo}.pdf'
        result_file = open(ruta, "w+b")
        usuario = Usuarios.objects.get(pk = request.user.pk)
        data = {
            'usuario': usuario,
            'fecha': datetime.datetime.now().date(),
            'encabezado' : f'{settings.STATIC_URL}images/encabezado.jpg',
            'imagenCentro' : f'{settings.STATIC_URL}images/imagenCentro.jpg',
            'piePagina' : f'{settings.STATIC_URL}images/piePagina.jpg'
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{nombreArchivo}.pdf"'
        template = get_template(f'{entidad}/{nombreArchivo}.html')

        html = template.render(data)
         # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response,
        link_callback=self.link_callback
        )
        #Guardar PDF
        pisa_status = pisa.CreatePDF(
        html, dest=result_file,
        link_callback=self.link_callback
        )
        try:
            path = Path(ruta)
            with path.open(mode='rb') as f:
                archivoCargado= File(f, name=path.name)
                doc = SeguimientoDocumentacion.objects.create(idUsuario =  request.user, archivo = archivoCargado)
                doc.save()
        except Exception as e:
            print('Error_ ', e)
        result_file.close() 
        pisa_status = pisa.CreatePDF(
        html, dest=response,
        link_callback=self.link_callback
        )
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class listadoSolicitudes(LoginRequiredMixin, ListView):
    model = SeguimientoDocumentacion
    template_name = f'{entidad}/solicitudes.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids = ''
        for i in self.model.objects.all().exclude(estado = True):
            ids += str(i.pk) + ','
        context['encabezado'] = ['#', 'Nombre del Documento solicitado', 'Solicitado Por', 'Fecha Solicitud', 'Fecha Actualización','Aprobar','Documento']
        context['title'] = 'Solicitudes'
        context['listado'] = 'Listado de Solicitudes Pendientes'
        context['idSeguimiento'] = ids
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            id = request.POST['id']
            estado = bool(request.POST['estado'])
            actualizar = SeguimientoDocumentacion.objects.get(pk = id)
            actualizar.estado = estado
            actualizar.save()
            data.append({'info':'Datos Guardados'})
            return JsonResponse(data, safe=False)
        except Exception as e:
            pass
        try:
            cont = 1
            for i in self.model.objects.all().exclude(estado = True):
                estado = 'checked' if i.estado else ''
                data.append([
                    cont,
                    i.idDocumento.nombre,
                    i.idUsuario.getInformacion(),
                    i.fechaCreacion.strftime("%Y-%m-%d %H:%M:%S"),
                    i.fechaModificacion.strftime("%Y-%m-%d %H:%M:%S") if i.fechaModificacion else 'Sin Cambios',
                    f'<div class="form-check form-switch"><input onClick="guardarAprobacion({i.pk})" name="{i.pk}" {estado} class="form-check-input" type="checkbox" id="guardarSolicitud{i.pk}"></div>',
                    'descargarArchivo',
                    i.archivo.url,
                    i.pk
                ])
                cont +=1
        except Exception as e:
            print(f'Error {entidad} ln-324: ',e)
            data = {}
        return JsonResponse(data, safe=False)
