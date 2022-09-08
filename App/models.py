from urllib import request
from django.db import models
from django.db.models.deletion import CASCADE
from uicApp.settings import *
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from django.core import validators
from django.utils.deconstruct import deconstructible
# Registro de los modelos de la base de datos
class Facultad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Facultad', primary_key=True)
    sigla = models.CharField(max_length=20, verbose_name='Nombre corto de la Facultad')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)

class Carrera(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Carrera', primary_key=True)
    idFacultad = models.ForeignKey(Facultad, verbose_name='Facultad', on_delete=CASCADE)
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
#Creación de usuarios para la administración del sitio Web
class Perfiles(models.Model):
    nombre = models.CharField(max_length=20, verbose_name='Perfiles', primary_key=True)
    def __str__(self) -> str:
        return '{}'.format(self.nombre)
class Usuarios(AbstractUser):
    @deconstructible
    class UnicodeUsernameValidator(validators.RegexValidator):
        regex = r'^[\w.@+-]+\Z'
        message = (
            'Enter a valid username. This value may contain only letters, '
            'numbers, and @/./+/-/_ characters.'
        )
        flags = 0
    imagen = models.ImageField(verbose_name='Imagen', upload_to='users', null = True, blank = True)
    perfil = models.ForeignKey(Perfiles, verbose_name='Perfil', default='Estudiante', on_delete=CASCADE, null=True, blank=True)
    celular = models.CharField(max_length=10, verbose_name='Celular')
    username_validator = UnicodeUsernameValidator
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE, null=True, blank=True)
    username = models.CharField(
        ('Usuario'),
        max_length=13,
        unique=True,
        help_text=('Se requiere al menos 10 catacteres'),
        validators=[username_validator],
        error_messages={
            'unique': ("Un usuario con esta cédula ya se encuentra registrado"),
        },
    )   
    def getImagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'images/default.jpg')
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    def getInformacion(self):
        return '{} {}'.format(self.first_name, self.last_name)
    def clean(self):
        super().clean()
    

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
class Nivel(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Nivel')
    periodoInicio = models.DateField( verbose_name='Periodo de inicio de Proyecto')
    periodoFin = models.DateField( verbose_name='Periodo de fin de Proyecto', null = True, blank = True)
    periodoActual = models.DateField( verbose_name='Periodo Actual')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)

class Proyecto(models.Model):
    usuarios = []
    for user in Usuarios.objects.all():
        nombre = user.getInformacion()
        if user.perfil.nombre == 'Docente':
            usuarios.append((str(user.pk), nombre))
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE)
    idNivel = models.ForeignKey(Nivel, verbose_name='Nivel', on_delete=CASCADE)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Proyecto')
    idDocente = models.CharField(choices=usuarios, verbose_name='Docente', max_length=13)
    idEstudiantes = models.ManyToManyField(Usuarios, verbose_name='Listado de Estudiantes')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
    def getEstudiantes(self):
        ul = '<li>'
        for estudiante in self.idEstudiantes.all():
            ul += f'<ul> {estudiante} </ul>'
        ul += '</ul>'
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
class Imagenes(models.Model):
    nombre = models.CharField(max_length=10, verbose_name='Nombre')
    imagen = models.ImageField(verbose_name='Imagen', upload_to='informacion', null = True, blank = True)
    def __str__(self) -> str:
        return '{}'.format(self.nombre)

class Informacion(models.Model):
    nombre = models.CharField(max_length=10, verbose_name='Nombre')
    detalle = models.TextField(max_length=100, verbose_name='Detalles', null = True, blank = True)
    imagen = models.ManyToManyField(Imagenes,verbose_name='Imagen', blank = True)
    def __str__(self) -> str:
        return '{} {}'.format(self.nombre, self.detalle)
class Tutoria(models.Model):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    descripcion = models.TextField(verbose_name='Temas a tratarse')
    fecha = models.DateTimeField(verbose_name='Fecha y hora de tutoría')
    archivo = models.FileField(upload_to='tutorias', null = True, blank = True, verbose_name='Archivo de Tutoría')
    def __str__(self):
        return self.descripcion


    
    
    
