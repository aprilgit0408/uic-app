from django.db import models
from django.db.models.deletion import CASCADE
from Usuarios.models import Carrera, Perfiles, Usuarios
from crum import get_current_request
# Registro de los modelos de la base de datos

class ListaVerificacion(models.Model):
    detalles = [
        (1,'Solicitud de opción de titulación/Certificado de idoneidad.'),
        (2,'Oficio o correo electrónico de llamado para elaborar el cronograma.'),
        (3,'Cronograma de trabajo.')
    ]
    idEstudiante = models.ForeignKey(Usuarios, verbose_name='Estudiante', on_delete=CASCADE)
    nombreArchivo = models.PositiveIntegerField(verbose_name='Detalle', choices=detalles)
    cumplimiento = models.BooleanField(default=False, verbose_name='Cumplimiento')
    observacion = models.TextField(max_length=100, verbose_name='Observación', null = True, blank = True)
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def getNombreArchivo(self):
        return f'{self.detalles[self.nombreArchivo][1]}'


class Proyecto(models.Model):
    usuarios = []
    try:
        for user in Usuarios.objects.all():
            nombre = user.getInformacion()
            if user.perfil:
                if user.perfil.nombre == 'Docente':
                    usuarios.append((str(user.pk), nombre))
    except:
        print('No hay perfiles')
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Proyecto')
    idDocente = models.CharField(choices=usuarios, verbose_name='Docente', max_length=13)
    idEstudiantes = models.ManyToManyField(Usuarios, verbose_name='Listado de Estudiantes')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
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

class Avance(models.Model):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    nombreAvance = models.CharField(max_length=100, verbose_name='Nombre Avance')
    observacion = models.CharField(max_length=100, verbose_name='Observacion')
    porcentaje = models.PositiveIntegerField(verbose_name='Porcentaje completado')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombreAvance)
class Tribunal(models.Model):
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
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0} - {1}'
        return txt.format(self.aula, self.fechaDefensa)
class Tutoria(models.Model):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    descripcion = models.TextField(verbose_name='Temas a tratarse')
    fecha = models.DateTimeField(verbose_name='Fecha y hora de tutoría')
    archivo = models.FileField(upload_to='tutorias', null = True, blank = True, verbose_name='Archivo de Tutoría')
    def __str__(self):
        return self.descripcion
class GrupoExperto(models.Model):
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
class Documento(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Documento', primary_key=True)
    archivo = models.FileField(verbose_name='Archivo', upload_to='documentacion')
    idPerfiles = models.ManyToManyField(Perfiles, verbose_name='Disponible para')    
    def __str__(self):
        return self.nombre
