from datetime import datetime
from django.template.loader import render_to_string
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
from Usuarios.models import Carrera, Constantes, Usuarios, Documento, SeguimientoDocumentacion
from uicApp.settings import TIME_ZONE
from App.funciones import getDate, send_mail, funcionGenerarPDF
from pathlib import Path
from django.utils.encoding import uri_to_iri
from django.core.files import File
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
        context['encabezado'] = ['#','proyecto', 'Docentes Principales', 'Docentes Suplentes', 'Fecha defensa', 'aula']
        context['title'] = f'{entidad}'
        context['listado'] = f'Listado de {entidad}es asignados'
        return context
    def post(self, request, *args, **kwargs):
        data = []
        try:
            cont = 1
            for i in modelo.objects.all():
                data.append([
                    cont,
                    i.idProyecto.nombre,
                    i.getDocentesPrincipales(),
                    i.getDocentesSuplentes(),
                    getDate(i.fechaDefensa),
                    i.aula,
                    i.pk
                ])
                cont +=1
        except Exception as e:
            print(f'Error {entidad} l-52 ',e)
            data = {}
        return JsonResponse(data, safe=False)


class addTribunal(LoginRequiredMixin, ListView):
    model = modelo
    form_class = formulario
    template_name = main
    success_url = url
    def guardarDocumentosGenerados(self, usuario, datosAdicionales, id):
        try:    
            path = Path(datosAdicionales['archivo']['ruta'])
            with path.open(mode='rb') as f:
                archivoCargado= File(f, name=path.name)
                documento = Documento.objects.get(id = id)
                doc = SeguimientoDocumentacion.objects.create(idDocumento = documento,idUsuario = usuario, archivo = archivoCargado, estado = True)
                doc.save() 
        except Exception as e:
            print('Error al guardar el archivo generado ln-114: ', e)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            idCarrera = request.POST['idCarrera']
            proyectos = Proyecto.objects.filter(idCarrera = idCarrera)
            for proyecto in proyectos:
                data.append(proyecto.toJSON())
            return JsonResponse(data, safe=False)
        except Exception as e:
            print('Error : 73: ', e)
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
            proyecto = Proyecto.objects.get(pk = int(idProyecto))
            anexo_id = 16 if proyecto.defensa else 15
            anexo = f'Anexo_{anexo_id}'
            docSuplentes = DocentesSuplente.objects.create(uuID = uuID)
            DOC_SUP = []
            for ds in idDocentesSuplentes.split(','):
                docentePrincipal_id = Usuarios.objects.get(pk = int(ds))
                DOC_SUP.append(docentePrincipal_id)
            docSuplentes.docentesSuplentes.set(DOC_SUP)
            docSuplentes.save()
            DOC_PRIN = []
            
            for ds in idDocentesPrincipales.split(','):
                docentePrincipal_id = Usuarios.objects.get(pk = int(ds))
                DOC_PRIN.append(docentePrincipal_id)
            tribunal = Tribunal.objects.create(idProyecto = proyecto, docentesSuplentes = DocentesSuplente.objects.get(pk = uuID), fechaDefensa = idFecha, aula = idAula)
            tribunal.docentesPrincipales.set(DOC_PRIN)
            tribunal.save()

            tipoDefensa = 'defensa' if proyecto.defensa else 'predefensa'
            mailDocentesPrincipales = tribunal.getMailDocPrincipales()
            mailDocentesSuplentes = tribunal.getMailDocSuplentes()
            mailEstudianteTribunal = proyecto.getMailEstudiantes()
            idSecuencial = Constantes.objects.get(nombre = 'SEC_MEM')
            secretarioGeneral = Constantes.objects.get(nombre = 'SEC_GEN')
            datosAdicionales = {
                        'year': datetime.now().year,
                        'secuencial': idSecuencial.valor,
                        'tribunal': tribunal,
                        'secretarioGeneral': secretarioGeneral.valor
                    }
            sendMail = {}
            sendMail['asunto'] = f'Asignacion del tribunal de {tipoDefensa}'
            sendMail['destinatarios'] = mailDocentesPrincipales
            content = render_to_string('email.html',
                                       {'titulo': f'Asignación de Tribunal de {tipoDefensa} de Proyectos', 
                                       'tema': 'sido asignado como uno de los docentes principales', 
                                       'proyecto':proyecto.nombre, 
                                       'docentesPrincipales' : tribunal.getDocentesPrincipales(),
                                       'fechaDefensa' : getDate(tribunal.fechaDefensa),
                                       'aula' : tribunal.aula
                                       })
            sendMail['content'] = content
            url_firma = uri_to_iri(Usuarios.objects.get(pk = request.user.pk).firma.firmaUsuario.url)
            funcionGenerarPDF("ASIGNACION_TRIBUNAL", anexo, request, "", datosAdicionales,  247, 100,url_firma, sendMail)
            for doce_prin in DOC_PRIN:
                self.guardarDocumentosGenerados(doce_prin,datosAdicionales, anexo_id)
            content = render_to_string('email.html',
                                       {'titulo': f'Asignación de Tribunal de {tipoDefensa} de Proyectos', 
                                       'tema': 'sido asignado como uno de los docentes suplentes', 
                                       'proyecto':proyecto.nombre, 
                                       'docentesSuplentes' : tribunal.getDocentesSuplentes(),
                                       'fechaDefensa' : getDate(tribunal.fechaDefensa),
                                       'aula' : tribunal.aula
                                       })
            sendMail['destinatarios'] = mailDocentesSuplentes
            sendMail['content'] = content
            funcionGenerarPDF("ASIGNACION_TRIBUNAL", anexo, request, "", datosAdicionales, 247, 100,url_firma, sendMail)
            for doce_sup in DOC_SUP:
                self.guardarDocumentosGenerados(doce_sup,datosAdicionales, anexo_id)
            content = render_to_string('email.html',
                                       {'titulo': f'Asignación de Tribunal de {tipoDefensa} de Proyectos', 
                                       'tema': 'sido asignado como uno de los docentes suplentes', 
                                       'proyecto':proyecto.nombre, 
                                       'docentesSuplentes' : tribunal.getDocentesSuplentes(),
                                       'fechaDefensa' : getDate(tribunal.fechaDefensa),
                                       'aula' : tribunal.aula
                                       })
            sendMail['content'] = content
            sendMail['destinatarios'] = mailEstudianteTribunal
            funcionGenerarPDF("ASIGNACION_TRIBUNAL", anexo, request, "", datosAdicionales,247, 100,url_firma, sendMail)
            for estudiantes_id in proyecto.idEstudiantes.all():
                self.guardarDocumentosGenerados(estudiantes_id,datosAdicionales, anexo_id)
            idSecuencial.valor = str(int(idSecuencial.valor) + 1)
            idSecuencial.save()
        except Exception as e:
            print('Sin valores a agregar: ', e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docentes = Usuarios.objects.filter(perfil__nombre = 'Docente')
        aulas = Constantes.objects.get(nombre = 'AULAS').valor
        data = []
        for user in docentes:
            data.append({'pk': user.pk, 'user': user})
        context['title'] = f'{entidad}'
        context['accion'] = f'Añadir {entidad}'
        context['agregar'] = f'Añadir {entidad}'
        context['URL'] = url
        context['listadoDocentes'] = data
        context['AULAS'] = aulas.split(',')
        context['idCarreras'] = Carrera.objects.all()
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
        data = []
        try:
            usuarios = request.POST['usuarios']
            usuarios = usuarios.split(',')
            for user in usuarios:
                data.append({'pk' : user, 'user' : Usuarios.objects.get(pk = int(user)).getInformacion()})
        except Exception as e:
            print('Sin valor para usuario: ', e)
        
        try:
            instance = modelo.objects.get(pk = self.kwargs['pk'])
            idDocentesPrincipales = request.POST['idDocentesPrincipales']
            idDocentesSuplentes = request.POST['idDocentesSuplentes']
            idAula = request.POST['idAula']
            idFecha = parse_datetime(request.POST['idFecha'])
            idFecha.replace(tzinfo=ZoneInfo(TIME_ZONE))
            docSuplentes = DocentesSuplente.objects.get(uuID = instance.docentesSuplentes.pk)
            DOC_SUP = []
            for ds in idDocentesSuplentes.split(','):
                DOC_SUP.append(Usuarios.objects.get(pk = int(ds)))
            docSuplentes.docentesSuplentes.set(DOC_SUP)
            docSuplentes.save()
            DOC_PRIN = []
            for ds in idDocentesPrincipales.split(','):
                DOC_PRIN.append(Usuarios.objects.get(pk = int(ds)))
            instance.fechaDefensa = idFecha
            instance.aula = idAula
            instance.docentesPrincipales.set(DOC_PRIN)
            instance.save()
            mailDocentesPrincipales = instance.getMailDocPrincipales()
            mailDocentesSuplentes = instance.getMailDocSuplentes()
            content = render_to_string('email.html',
                                       {'titulo': 'Actualización de Tribunal de {tipoDefensa} de Proyectos', 
                                       'tema': 'sido asignado como uno de los docentes principales', 
                                       'proyecto':instance.idProyecto.nombre, 
                                       'docentesPrincipales' : instance.getDocentesPrincipales(),
                                       'fechaDefensa' : getDate(instance.fechaDefensa),
                                       'aula' : instance.aula
                                       })
            send_mail('Actualización de Tribunal', mailDocentesPrincipales, content)
            content = render_to_string('email.html',
                                       {'titulo': 'Actualización de Tribunal de {tipoDefensa} de Proyectos', 
                                       'tema': 'sido asignado como uno de los docentes suplentes', 
                                       'proyecto':instance.idProyecto.nombre, 
                                       'docentesSuplentes' : instance.getDocentesSuplentes(),
                                       'fechaDefensa' : getDate(instance.fechaDefensa),
                                       'aula' : instance.aula
                                       })
            send_mail('Actualización de Tribunal', mailDocentesSuplentes, content)
        except Exception as e:
            print('Sin valores a agregar: ', e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        instance = modelo.objects.get(pk = self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        docentes = Usuarios.objects.filter(perfil__nombre = 'Docente')
        aulas = Constantes.objects.get(nombre = 'AULAS').valor
        data = []
        for user in docentes:
            data.append({'pk': user.pk, 'user': user})
        context['title'] = f'{entidad}'
        context['agregar'] = f'Añadir {entidad}'
        context['URL'] = url
        context['listadoDocentes'] = data
        context['AULAS'] = aulas.split(',')
        context['instance'] = instance
        context['DOC_PRIN'] = Constantes.objects.get(nombre = 'DOC_PRIN').valor
        context['DOC_SUP'] = Constantes.objects.get(nombre = 'DOC_SUP').valor
        context['DATE'] = datetime.now()
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
        suplentes = DocentesSuplente.objects.get(pk = instance.docentesSuplentes.uuID)
        mailDocentesPrincipales = instance.getMailDocPrincipales()
        mailDocentesSuplentes = instance.getMailDocSuplentes()
        content = render_to_string('email.html',
                                       {'titulo': 'Actualización de Tribunal de {tipoDefensa} de Proyectos', 
                                       'tema': 'sido eliminada la asignación de defensa', 
                                       'proyecto': instance.idProyecto.nombre,
                                       'fechaDefensaEliminada' : getDate(instance.fechaDefensa),
                                       'aula' : instance.aula
                                       })
        send_mail('Actualización de Tribunal', mailDocentesPrincipales, content)
        content = render_to_string('email.html',
                                    {'titulo': 'Actualización de Tribunal de {tipoDefensa} de Proyectos', 
                                    'tema': 'sido eliminada la asignación de defensa', 
                                    'proyecto':instance.idProyecto.nombre, 
                                    'fechaDefensaEliminada' : getDate(instance.fechaDefensa),
                                    'aula' : instance.aula
                                    })
        send_mail('Actualización de Tribunal', mailDocentesSuplentes, content)
        suplentes.delete() 
        instance.delete()
        return JsonResponse(data, safe=False)
