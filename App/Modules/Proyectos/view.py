from django.views.generic import CreateView, ListView   
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from App.Modules.Formularios.forms import formularioDocentes, formularioProyectos, formularioUsuarios
from App.models import Proyecto, Tribunal
from pathlib import Path
from django.core.files import File
from Usuarios.models import Constantes, Usuarios, GeneracionFirmas, Documento, SeguimientoDocumentacion
from django.http.response import JsonResponse
from App.funciones import funcionGenerarPDF, getFecha
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.encoding import uri_to_iri

from datetime import datetime
import uuid
import qrcode
from os import remove

modelo = Proyecto
formulario = formularioProyectos
entidad = 'Proyectos'
main = 'main.html'
url = reverse_lazy(f'app:{entidad.lower()}')
class listarProyectos(LoginRequiredMixin, ListView):
    model = modelo
    template_name = f'{entidad}/listado.html'
    def dispatch(self, request, *args, **kwargs):
        #Generacion de firmas
        for usuario in Usuarios.objects.filter(firma = None):
            try:
                dominioActual = Constantes.objects.get(nombre = 'DOMINIO').valor
                uuIDFirma = str(uuid.uuid4())
                nombreArchivo = f'{usuario.username}_{usuario.last_name}_{usuario.pk}.png'
                firmaQR = f'**********************************'
                firmaQR += f'**********************************\n'
                firmaQR += 'SISTEMA DE INTEGRACION CURRICULAR\n'
                firmaQR += '*** FIRMADO POR ***\n'
                firmaQR += f'Cédula: {usuario.username}.\n'
                firmaQR += f'Nombres: {usuario.first_name}.\n'
                firmaQR += f'Apellidos: {usuario.last_name}.\n'
                firmaQR += 'Universidad Politécnica Estatal del Carchi.\n'
                firmaQR += f'{dominioActual}/validarFirmaUIAP/{uuIDFirma}\n'
                firmaQR += f'**********************************'
                firmaQR += f'**********************************\n'
                img = qrcode.make(firmaQR)
                firmaSave = open(nombreArchivo, "wb")
                img.save(firmaSave)
                firmaSave.close()
                path = Path(nombreArchivo)
                with path.open(mode='rb') as f:
                    archivoCargado= File(f, name=path.name)
                    generarFirma = GeneracionFirmas.objects.create(
                                    uuIDFirma = uuIDFirma,
                                    firmaUsuario = archivoCargado,
                                    idUsuario = usuario.pk)
                    generarFirma.save()
                    f.close()
                    usuario.firma = generarFirma
                    usuario.save()
                    remove(nombreArchivo)
            except Exception as e:
                print('Error al guardar el archivo generado ln-218: ', e)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        esEstudiante = True if self.request.user.perfil.nombre == 'Estudiante' else False
        context['encabezado'] = ['#', 'carrera','tema de investigación','estudiantes asignados'] if not esEstudiante else ['carrera','tema de investigación'] 
        context['title'] = f'{entidad}' 
        context['listado'] = f'Listado de {entidad}' 
        context['DATE'] = datetime.now()
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            admin = True if request.user.perfil.nombre == 'Admin' else False
            esEstudiante = True if request.user.perfil.nombre == 'Estudiante' else False
            if esEstudiante:
                query = modelo.objects.filter(idEstudiantes__pk = request.user.pk)
            else:
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
                        'SC',
                        i.id,
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
    def generarPDFTutor(self, docenteTutor, idsEstudiantes, nombreProyecto, carrera) :
        def sendMailHilos(estudiante):
            idSecuencial = Constantes.objects.get(nombre = 'SEC_MEM')
            data = {
                'tutor': docenteTutor.getInformacion(),
                'nombreEstudiante': estudiante.getInformacion(),
                'cedulaEstudiante': estudiante.username,
                'secuencial':idSecuencial.valor,
                'nombreCarrera': carrera
            }
            content = render_to_string('email.html',
                                       {'titulo': 'Asignación de Tutor', 
                                       'docente': self.request.user.getInformacion(), 
                                       'tema': ' generado un documento donde se ha seleccionado el tutor', 
                                       'proyecto':nombreProyecto,  
                                       })
            sendMail = {}
            sendMail['asunto'] = f'Asignación de tutor del proyecto "{nombreProyecto}"'
            sendMail['destinatarios'] = f'{docenteTutor.email},{estudiante.email}'
            sendMail['content'] = content
            url_firma = uri_to_iri(Usuarios.objects.get(pk = self.request.user.pk).firma.firmaUsuario.url)
            funcionGenerarPDF("ASIGNACION_TUTOR", "Anexo_7", self.request, "", data, 247, 225, url_firma, sendMail)
            estudiante.memorandoTutor = idSecuencial.valor
            estudiante.save()
            idSecuencial.valor = str(int(idSecuencial.valor) + 1)
            idSecuencial.save()
            try:    
                print('Archivo data ruta', data['archivo']['ruta'])
                path = Path(data['archivo']['ruta'])
                with path.open(mode='rb') as f:
                    archivoCargado= File(f, name=path.name)
                    documento = Documento.objects.get(id = 7)
                    doc = SeguimientoDocumentacion.objects.create(idDocumento = documento,idUsuario = estudiante, archivo = archivoCargado, estado = True)
                    doc.save() 
            except Exception as e:
                print('Error al guardar el archivo generado ln-114: ', e)
        for estudiante in idsEstudiantes.all():
            sendMailHilos(estudiante)
    def post(self, request, *args, **kwargs):
        form = formulario(request.POST)
        if form.is_valid():
            nombreProyecto = form.cleaned_data['nombre']
            idDocente = form.cleaned_data['idDocente']
            idEstudiantes = form.cleaned_data['idEstudiantes']
            idCarrera = form.cleaned_data['idCarrera']
            docenteTutor = Usuarios.objects.get(pk = idDocente)
            self.generarPDFTutor(docenteTutor, idEstudiantes, nombreProyecto, idCarrera.nombre)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        usuarios = []
        try:
            for user in Usuarios.objects.all():
                nombre = user.getInformacion()
                if user.perfil:
                    if user.perfil.nombre == 'Docente':
                        usuarios.append(user)
        except:
            pass
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        context['IDDocentes'] = usuarios
        context['idEstudiantes'] = Usuarios.objects.filter(perfil__nombre = 'Estudiante')
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
        for i in Usuarios.objects.filter(perfil__nombre = 'Estudiante'):
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
        context['encabezado'] = ['#', 'cédula', 'Nombre y Apellido', 'correo electrónico', 'teléfono', 'carrera','cohorte', 'fotografía']
        context['title'] = 'Estudiantes'
        context['listado'] = f'Listado de Estudiantes'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            listadoEstudiantes = []
            admin = True if request.user.perfil.nombre == 'Admin' else False
            query = Usuarios.objects.filter(perfil__nombre = 'Estudiante') if admin else modelo.objects.filter(idDocente = request.user.pk)
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
                    i.cohorte.cohorte if i.cohorte is not None else '-',
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
        context['title'] = 'Docentes'
        context['listado'] = f'Listado de Docentes'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            for i in Usuarios.objects.filter(perfil__nombre = 'Docente'):
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
class addDocente(LoginRequiredMixin, CreateView):
    model = Usuarios
    form_class = formularioDocentes
    template_name = 'main.html'
    success_url = reverse_lazy(f'app:docentes')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agregar'] = f'Añadir Docentes'
        context['accion'] = f'Añadir Docentes'
        context['title'] = f'Docentes'
        return context
class addEstudiantes(LoginRequiredMixin, CreateView):
    model = Usuarios
    form_class = formularioUsuarios
    template_name = 'main.html'
    success_url = reverse_lazy(f'app:estudiantes')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agregar'] = f'Añadir Estudiante'
        context['accion'] = f'Añadir Estudiante'
        context['title'] = f'Docentes'
        return context
    
class guardarDocumento(LoginRequiredMixin, TemplateView):
    template_name = main
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        idProyecto = request.POST['id']
        getFechaSolicitud = request.POST['fechaSolicitud']
        fechaSolicitud = getFecha(getFechaSolicitud)
        proyecto = Proyecto.objects.get(id = idProyecto)
        for estProyecto in proyecto.idEstudiantes.all():
            data = {
                'proyecto': proyecto,
                'estudiante': estProyecto,
                'fechaCronograma': fechaSolicitud,
                'tutor': request.user
            }
            content = render_to_string('email.html',
                                        {'titulo': 'Solicitud Cronograma', 
                                        'docente': request.user.getInformacion(), 
                                        'tema': 'solicitado el cronograma', 
                                        'proyecto':proyecto.nombre,
                                        'fechaEntrega' : fechaSolicitud  
                                        })
            
            sendMail = {}
            sendMail['asunto'] = 'Solicitud de Cronograma de Proyecto'
            sendMail['destinatarios'] = estProyecto.email
            sendMail['content'] = content
            if estProyecto.memorandoTutor is None:
                idSecuencial = Constantes.objects.get(nombre = 'SEC_MEM')
                estProyecto.memorandoTutor = idSecuencial.valor
                estProyecto.save()
                idSecuencial.valor = str(int(idSecuencial.valor) + 1)
                idSecuencial.save()
            url_firma = uri_to_iri(request.user.firma.firmaUsuario.url)
            funcionGenerarPDF("Solicitud_Cronograma", "Anexo_9", request, "", data,247,150,url_firma, sendMail)
            try:    
                path = Path(data['archivo']['ruta'])
                with path.open(mode='rb') as f:
                    archivoCargado= File(f, name=path.name)
                    documento = Documento.objects.get(id = 9)
                    doc = SeguimientoDocumentacion.objects.create(idDocumento = documento,idUsuario = estProyecto, archivo = archivoCargado, estado = True)
                    doc.save() 
            except Exception as e:
                print('Error al guardar el archivo generado ln-371: ', e)
        return JsonResponse([], safe=False)


class generarPDFProyecto(ListView):
    def get(self, request, *args, **kwargs) :
        
        proyecto = Proyecto.objects.get(id = 46)
        estudiante = None
        for estProyecto in proyecto.idEstudiantes.all():
            if estudiante is None:
                estudiante = estProyecto
                

        data = {
            'proyecto': Proyecto.objects.get(id = 46),
            'estudiante': estudiante,
            'fechaCronograma': datetime.now(),
            'horaCronograma': datetime.now().time,
            'tutor': request.user,
            'tribunal': Tribunal.objects.get(pk = 21)
        }
        content = render_to_string('email.html',
                                       {'titulo': 'Avances', 
                                       'docente': request.user.getInformacion(), 
                                       'tema': ' generado un documento donde se ha seleccionado el tutor', 
                                       'proyecto':'Hola mundo buen día',  
                                       })
        
        sendMail = {}
        sendMail['asunto'] = 'Asignacion de tutor'
        sendMail['destinatarios'] = 'josaerick@gmail.com'
        sendMail['content'] = None
        return funcionGenerarPDF("ASIGNACION_Tutor", "1", request, "", data, 247, 80, None, None)
        return super().get(request, *args, **kwargs)
