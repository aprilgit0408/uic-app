from email.policy import default
from django.db import models
from django.db.models.deletion import CASCADE
from Usuarios.models import Carrera, Constantes, Usuarios
from crum import get_current_user
from django.utils import timezone
from django.forms import model_to_dict

# Registro de los modelos de la base de datos

class datosAuditoria(models.Model):
    fechaCreacion = models.DateTimeField(editable=False, null=True, blank=True, default=timezone.now)
    fechaModificacion = models.DateTimeField(editable=False, null=True, blank=True)
    usuarioRegistro = models.PositiveIntegerField(editable=False, null=True, blank=True)
    usuarioModificacion = models.PositiveIntegerField(editable=False, null=True, blank=True)
    class Meta:
        abstract = True
    def setDatosAuditoria(self):
        request = get_current_user()
        if not self.fechaCreacion:
            self.fechaCreacion = timezone.now()
        else:
            self.fechaModificacion = timezone.now()
        #Setear Usuario Registro
        if not self.usuarioRegistro:
            self.usuarioRegistro = request.pk
        else:
            self.usuarioModificacion = request.pk
        return self
    
class Proyecto(datosAuditoria):
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Proyecto')
    idDocente = models.PositiveIntegerField(verbose_name='Docente Tutor del Proyecto')
    idEstudiantes = models.ManyToManyField(Usuarios, verbose_name='Listado de Estudiantes')
    defensa = models.BooleanField(default = False, verbose_name = 'Proyecto listo para pre/defensa')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
    def getEstudiantes(self):
        ul = ''
        for estudiante in self.idEstudiantes.all():
            ul += f'<li title="{estudiante}"> {estudiante.getAlias()} </li>'
        ul = f'<ul>{ul}</ul>'
        return ul
    def getEstudiantesCompleto(self):
        ul = ''
        for estudiante in self.idEstudiantes.all():
            ul += f'<li title="{estudiante}"> {estudiante.getNombreCompleto()} </li>'
        ul = f'<ul>{ul}</ul>'
        return ul
    def getEstudiantesUnaLinea(self):
        datos = ''
        for estudiante in self.idEstudiantes.all():
            if datos:
                datos += f', {estudiante.getNombreCompleto()}'
            else: 
                datos = f'Sr./Srta. {estudiante.getNombreCompleto()}'
        return datos
    def getMailEstudiantes(self):
        mail = []
        for estudiante in self.idEstudiantes.all():
             mail.append(estudiante.email)
        return ','.join(mail)
    def getDocente(self):
        return Usuarios.objects.get(pk = self.idDocente)
    def getDocenteJSON(self):
        return Usuarios.objects.get(pk = self.idDocente).toJSON()
    def getTotalEstudiantes(self):
        return 's' if len(self.idEstudiantes.all()) > 1 else ''
    def getTitulo(self):
        genero = []
        for estudiante in self.idEstudiantes.all():
            if estudiante.genero is not genero:
                genero.append(estudiante.genero)
        tipo = ''
        titulo = ''
        if(self.idCarrera.tipoTitulo == 'Administrador Público'):
            titulo = 'A'
        elif(self.idCarrera.tipoTitulo == 'Ingeniería'):
            titulo = 'I'
        else:
            titulo = 'L'

        if len(genero) > 1:
            if(genero[0] == 'M'):
                if(titulo == 'A'):
                    tipo = 'Administradora Pública en '
                elif(titulo == 'I'):
                    tipo = 'Ingenieras en '
                else:
                    tipo = 'Licenciadas en '
            else:
                if(titulo == 'A'):
                    tipo = 'Administrador Público en '
                elif(titulo == 'I'):
                    tipo = 'Ingenieros en '
                else:
                    tipo = 'Licenciados en '
        else:
            if(genero[0]== 'H'):
                if(titulo == 'A'):
                    tipo = 'Administrador Público en '
                elif(titulo == 'I'):
                    tipo = 'Ingeniero en '
                else:
                    tipo = 'Licenciado en '
            else:
                if(titulo == 'A'):
                    tipo = 'Administradora Pública en '
                elif(titulo == 'I'):
                    tipo = 'Ingeniera en '
                else:
                    tipo = 'Licenciada en '
        return tipo
    
    def toJSON(self):
        txt = model_to_dict(self)
        if self.idEstudiantes:
            txt['idEstudiantes'] = None
        if self.idDocente:
            txt['idDocente'] = self.getDocenteJSON()
        return txt

    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
class NombreArchivoListaVerificacion(datosAuditoria):
    modalidades = [
        (1, 'Trabajo de Integración Curricular (TIC)'),
        (2, 'Examen con Carácter Complexivo (ECC)')
    ]
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    orden = models.PositiveIntegerField(null=True, blank=True)
    tipo = models.PositiveIntegerField(choices=modalidades, verbose_name='Modalidad', default=1)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
    class Meta:
        ordering = ['orden']
    def __str__(self):
        return f'{self.nombre}'

class ListaVerificacion(datosAuditoria):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    nombre = models.ForeignKey(NombreArchivoListaVerificacion, verbose_name='Nombre del Archivo', on_delete=CASCADE)
    archivo = models.FileField(verbose_name='Archivo',upload_to='listaVerificacion')
    observacion = models.TextField(max_length=100, verbose_name='Observación', null = True, blank = True)
    idEstudiante = models.ForeignKey(Usuarios, on_delete=CASCADE, null=True, blank=True)
    estado = models.BooleanField(default=False, verbose_name='Cumplimiento')
    def getNombreArchivo(self):
        return f'{self.detalles[self.nombreArchivo][1]}'
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.nombre.nombre} -> Archivo admitido : {"(Si)" if self.estado else "(No)"}'

class Avance(datosAuditoria):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    nombreAvance = models.CharField(max_length=100, verbose_name='Nombre Avance')
    observacion = models.CharField(max_length=100, verbose_name='Observacion', blank=True, null=True)
    porcentaje = models.PositiveIntegerField(verbose_name='Porcentaje completado', default=0)
    archivo = models.FileField(verbose_name='Documento', upload_to='documentacion', blank=True, null=True)
    fechaEntrega = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombreAvance)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
class Tutoria(datosAuditoria):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    descripcion = models.TextField(verbose_name='Temas a tratarse')
    fechaTutoria = models.DateTimeField(verbose_name='Fecha y hora de tutoría')
    archivo = models.FileField(upload_to='tutorias', null = True, blank = True, verbose_name='Archivo de Tutoría')
    def __str__(self):
        return self.descripcion
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
        
class DocentesSuplente(datosAuditoria):
    uuID = models.CharField(max_length = 36, primary_key=True) 
    docentesSuplentes= models.ManyToManyField(Usuarios, verbose_name='Docentes Principales')
    # def __str__(self):
    #     docentes = ''
    #     for doc in self.docentesSuplentes.all():
    #         if docentes:
    #             docentes += f', {doc}'
    #         else:
    #             docentes = doc
    #     return docentes

class Tribunal(datosAuditoria):
    aulas = []
    try:
        for i in (Constantes.objects.get(nombre = 'AULAS').valor).split(','):
            aulas.append((f'{i}', f'Aula {i}')) 
    except:
        pass
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    docentesPrincipales = models.ManyToManyField(Usuarios, verbose_name='Docentes Principales')
    docentesSuplentes = models.ForeignKey(DocentesSuplente, verbose_name='Docentes Principales', on_delete=CASCADE) 
    fechaDefensa = models.DateTimeField(null=True, blank=True, default=timezone.now)
    aula = models.CharField(choices=aulas,  max_length = 20, verbose_name='Aula de defensa asignada')
    def __str__(self) -> str:
        txt = '{0} - {1}'
        return txt.format(self.aula, self.fechaDefensa)
    def getDocentesPrincipales(self):
        ul = ''
        cont = 1
        for doc in self.docentesPrincipales.all():
            ul += f'<li title="{doc.getInformacion()}"> {cont}. {doc.getInformacion()} </li>'
            cont += 1
        ul = f'<ul>{ul}</ul>'
        return ul
    def getDocentesPrincipalesPDF(self):
        cargos = ['Presidente', 'Tutor', 'Docente']
        cont = 0
        data = []
        for doc in self.docentesPrincipales.all():
            data.append({'docente': doc.getInformacion(), 'cargo': cargos[cont]})
            cont += 1
        return data
    def getDocentesAlternosPDF(self):
        cargos = ['Presidente', 'Tutor', 'Docente']
        cont = 0
        data = []
        for doc in self.docentesSuplentes.docentesSuplentes.all():
            data.append({'docente': doc.getInformacion(), 'cargo': cargos[cont]})
            cont += 1
        return data
    def getMailDocPrincipales(self):
        mail = []
        for doc in self.docentesPrincipales.all():
            mail.append(doc.email)
        return ','.join(mail)
    def getDocentesSuplentes(self):
        ul = ''
        cont = 1
        for doc in self.docentesSuplentes.docentesSuplentes.all():
            ul += f'<li title="{doc.getInformacion()}"> {cont}. {doc.getInformacion()} </li>'
            cont += 1

        ul = f'<ul>{ul}</ul>'
        return ul
    def getMailDocSuplentes(self):
        mail = []
        for doc in self.docentesSuplentes.docentesSuplentes.all():
            mail.append(doc.email)
        return ','.join(mail)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
class ListaValidacionCarrera(datosAuditoria):
    nombreCarrera = models.ForeignKey(Carrera, on_delete=CASCADE)
    visulizacionCompleta = models.BooleanField(default=True) 
    nombreListaVer = models.ManyToManyField(NombreArchivoListaVerificacion, blank=True)