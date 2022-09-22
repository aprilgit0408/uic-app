from django.db import models
from django.db.models.deletion import CASCADE
from Usuarios.models import Carrera, Usuarios
from crum import get_current_user
from django.utils import timezone

# Registro de los modelos de la base de datos

class datosAuditoria(models.Model):
    fechaCreacion = models.DateTimeField(editable=False, null=True, blank=True, default=timezone.now)
    fechaModificacion = models.DateTimeField(editable=False, null=True, blank=True, default=timezone.now)
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
    
class ListaVerificacion(datosAuditoria):
    detalles = [
        (1,'Solicitud de opción de titulación/Certificado de idoneidad.'),
        (2,'Oficio o correo electrónico de llamado para elaborar el cronograma.'),
        (3,'Cronograma de trabajo.')
    ]
    idEstudiante = models.ForeignKey(Usuarios, verbose_name='Estudiante', on_delete=CASCADE)
    nombreArchivo = models.PositiveIntegerField(verbose_name='Detalle', choices=detalles)
    cumplimiento = models.BooleanField(default=False, verbose_name='Cumplimiento')
    observacion = models.TextField(max_length=100, verbose_name='Observación', null = True, blank = True)
    def getNombreArchivo(self):
        return f'{self.detalles[self.nombreArchivo][1]}'
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)


class Proyecto(datosAuditoria):
    usuarios = []
    try:
        for user in Usuarios.objects.all():
            nombre = user.getInformacion()
            if user.perfil:
                if user.perfil.nombre == 'Docente':
                    usuarios.append((str(user.pk), nombre))
    except:
        pass
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Proyecto')
    idDocente = models.CharField(choices=usuarios, verbose_name='Docente', max_length=13)
    idEstudiantes = models.ManyToManyField(Usuarios, verbose_name='Listado de Estudiantes')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
    def getEstudiantes(self):
        ul = ''
        for estudiante in self.idEstudiantes.all():
            ul += f'<li> {estudiante} </li>'
        ul = f'<ul>{ul}</ul>'
        return ul
    def getDocente(self):
        return Usuarios.objects.get(pk = self.idDocente)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)

class Avance(datosAuditoria):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    nombreAvance = models.CharField(max_length=100, verbose_name='Nombre Avance')
    observacion = models.CharField(max_length=100, verbose_name='Observacion', blank=True, null=True)
    porcentaje = models.PositiveIntegerField(verbose_name='Porcentaje completado', default=0)
    archivo = models.FileField(verbose_name='Documento', upload_to='documentacion', blank=True, null=True)
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombreAvance)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
class Tribunal(datosAuditoria):
    usuarios = []
    for user in Usuarios.objects.all():
        nombre = user.getInformacion()
        usuarios.append((user.pk, nombre))
    aulas = [
        (1, 'Aula 1'),
        (2, 'Aula 2'),
        (3, 'Aula 3'),
        (4, 'Aula 4'),
        (5, 'Aula 5'),
        (6, 'Aula 6'),
        (7, 'Aula 7'),
        (8, 'Aula 8'),
        (9, 'Aula 9')
        ]
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    primerDocente = models.CharField(choices=usuarios, max_length=15, verbose_name='Primer Docente')
    segundoDocente = models.CharField(choices=usuarios, max_length=15, verbose_name='Segundo Docente')
    terceroDocente = models.CharField(choices=usuarios, max_length=15, verbose_name='Tercer Docente')
    primerDocenteSuplente = models.CharField(choices=usuarios, max_length=15, verbose_name='Primer Docente Suplente')
    segundoDocenteSuplente = models.CharField(choices=usuarios, max_length=15, verbose_name='Segundo Docente Suplente')
    terceroDocenteSuplente = models.CharField(choices=usuarios, max_length=15, verbose_name='Tercer Docente Suplente')
    fechaDefensa = models.DateTimeField()
    aula = models.PositiveIntegerField(choices=aulas, verbose_name='Aula de defensa asignada')
    def __str__(self) -> str:
        txt = '{0} - {1}'
        return txt.format(self.aula, self.fechaDefensa)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)

class Tutoria(datosAuditoria):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    descripcion = models.TextField(verbose_name='Temas a tratarse')
    fecha = models.DateTimeField(verbose_name='Fecha y hora de tutoría')
    archivo = models.FileField(upload_to='tutorias', null = True, blank = True, verbose_name='Archivo de Tutoría')
    def __str__(self):
        return self.descripcion
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)

class GrupoExperto(datosAuditoria):
    nombre = models.CharField(max_length=40, verbose_name='Nombre del grupo', primary_key=True)
    idDocentes = models.ManyToManyField(Usuarios, verbose_name='Docentes')
    def __str__(self):
        return self.nombre
    def getMiembros(self):
        ul = ''
        for docentes in self.idDocentes.all():
            ul += f'<li> {docentes} </li>'
        ul = f'<ul>{ul}</ul>'
        return ul
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)