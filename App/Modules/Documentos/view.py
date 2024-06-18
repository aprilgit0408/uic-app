from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioDocumentos, formularioFirma, formActualizarfirma, ListaVerificacion
from django.views.generic.base import  View
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
import datetime
from django.shortcuts import redirect
import os
from django.core.files import File
from pathlib import Path
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Usuarios.models import SeguimientoDocumentacion, Usuarios, Documento
from django.utils.encoding import uri_to_iri
from uicApp import settings
from App.funciones import funcionGenerarPDF, idsListaVerificacionObl
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
    idNoGenerados = [7,9,15,16]
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
    def getEstado(self, estado, cont, datosEstado, documentacion):
        if estado == True or documentacion.id in self.idNoGenerados:
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
            valReqObliLisVer = ListaVerificacion.objects.filter(nombre__id__in = idsListaVerificacionObl(), idProyecto__idEstudiantes__id = self.request.user.pk, estado = True)
            puedeContinuar = False
            if len(valReqObliLisVer) == len(idsListaVerificacionObl()):
                puedeContinuar = True
            #la documentacion que tiene el usuario actual
            getDocumentacionBKP = SeguimientoDocumentacion.objects.filter(idUsuario = request.user.pk)
            valorAnterior = ''
            for documentacion in Documento.objects.all():
                for perfil in documentacion.idPerfiles.all():
                    if perfil.nombre == 'Estudiante':
                        #buscamos si el documento se encuentra a la documentacion con algun estado 
                        getDocumentoRegistrado = [seguimiento for seguimiento in getDocumentacionBKP if seguimiento and seguimiento.idDocumento == documentacion]
                        #validamos que el documento no sea uno de los id autogenerados
                        if len(getDocumentoRegistrado) == 0 and (documentacion.id in self.idNoGenerados or (puedeContinuar == False and documentacion.id != 1)):
                            continue
                        habilitar = getDocumentoRegistrado if getDocumentoRegistrado else False
                        estadoPantalla = habilitar[0].estado if habilitar else  False if valorAnterior else False if cont == 1 else''
                        getEstadoActual = self.getEstado(estadoPantalla, cont, getDocumentoRegistrado, documentacion)
                        extencionURL = documentacion.archivo.url.split('.')
                        data.append([
                            cont,
                            documentacion.nombre,
                            getEstadoActual,
                            'file',
                            estadoPantalla,
                            extencionURL[len(extencionURL) - 1],
                            documentacion.archivo.url if getEstadoActual != 'Aprobado' else getDocumentoRegistrado[0].archivo.url if getDocumentoRegistrado else '',
                            documentacion.pk
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
    def get(self, request, *args, **kwargs):
        try:
            idDocumeto = Documento.objects.get(pk = self.kwargs['pk'])
            nombreArchivo = idDocumeto.nombre
            templateID = idDocumeto.pk
            ruta = f'media/documentacionEstudiante/{request.user.getInformacion()}-{nombreArchivo}.pdf'
            result_file = open(ruta, "w+b")
            usuario = Usuarios.objects.get(pk = request.user.pk)
            data = {
                'usuario': usuario,
                'fecha': datetime.datetime.now().date(),
                'encabezado' : f'{settings.STATIC_URL}images/encabezado.jpg',
                'imagenCentro' : f'{settings.STATIC_URL}images/imagenCentro.jpg',
                'piePagina' : f'{settings.STATIC_URL}images/piePagina.jpg'
            }
            template = get_template(f'{entidad}/{templateID}.html')
            html = template.render(data)
            css_url = os.path.join(settings.BASE_DIR, 'static/css/bootstrap.min.css')
            HTML(string=html, base_url='').write_pdf(result_file, stylesheets=[CSS(css_url)])
            getRegistro = SeguimientoDocumentacion.objects.filter(idDocumento = idDocumeto.pk, idUsuario = request.user)
            if not getRegistro.exists():
                try:
                    path = Path(ruta)
                    with path.open(mode='rb') as f:
                        archivoCargado= File(f, name=path.name)
                        doc = SeguimientoDocumentacion.objects.create(idDocumento = idDocumeto,idUsuario =  request.user, archivo = archivoCargado)
                        doc.save() 
                except Exception as e:
                    print('Error al guardar el archivo generado ln-202: ', e)
            else:
                #Actualizar Documento
                try:
                    path = Path(ruta)
                    with path.open(mode='rb') as f:
                        archivoCargado= File(f, name=path.name)
                        doc = getRegistro[0]
                        doc.archivo = archivoCargado
                        doc.save()
                except Exception as e:
                    print('Error al Actualizar el archivo generado ln-213: ', e)
            result_file.close()
        except Exception as e:
            print('Error ln-185: ', e)
        return HttpResponseRedirect(url)
class generarPDF(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            documento = Documento.objects.get(pk = self.kwargs['pk'])
            nombreArchivo = documento.nombre
            templateArchivo = documento.id
            datosAdicionales = SeguimientoDocumentacion.objects.filter(idDocumento = documento, idUsuario = self.request.user.pk).first()
            url_firma = uri_to_iri(self.request.user.firma.firmaUsuario.url)
            return funcionGenerarPDF(nombreArchivo, templateArchivo, request, url, datosAdicionales, 247, 500, url_firma)
        except Exception as e:
            print('Error ln-200: ', e)
            return redirect(url)

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
    
class guardarSolicitud(LoginRequiredMixin, UpdateView):
    model = SeguimientoDocumentacion
    form_class = formActualizarfirma
    template_name = main
    success_url = reverse_lazy('app:solicitudes')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    def get_object(self, queryset = None):
        id = self.request.POST['id']
        seguimiento = SeguimientoDocumentacion.objects.get(id = id)
        return seguimiento
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)

