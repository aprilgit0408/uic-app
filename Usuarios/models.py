from django.utils import timezone
from django.db import models
from django import forms
from django.db.models.deletion import CASCADE
from uicApp.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth.models import AbstractUser
from crum import get_current_user
from django.forms import model_to_dict
from .validaciones import ValidarCedulaUsurio, getMeses
import uuid
import qrcode
from os import remove
from pathlib import Path
from django.core.files import File

class datosAuditoria(models.Model):
    fechaCreacion = models.DateTimeField(editable=False, null=True, blank=True, default=timezone.now)
    fechaModificacion = models.DateTimeField(editable=False, null=True, blank=True)
    usuarioRegistro = models.PositiveIntegerField(editable=False, null=True, blank=True)
    usuarioModificacion = models.PositiveIntegerField(editable=False, null=True, blank=True)
    class Meta:
        abstract = True
    def setDatosAuditoria(self):
        if not self.fechaCreacion:
            self.fechaCreacion = timezone.now()
        else:
            self.fechaModificacion = timezone.now()
        #Setear Usuario Registro
        try:
            request = get_current_user()
            if not self.usuarioRegistro:
                self.usuarioRegistro = request.pk
            else:
                self.usuarioModificacion = request.pk
            return self
        except:
            pass

class Facultad(datosAuditoria):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Facultad', unique = True)
    sigla = models.CharField(max_length=20, verbose_name='Nombre corto')
    def __str__(self) -> str:
        return self.nombre
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)

class Carrera(datosAuditoria):
    tipoTitulos = [
        ('Ingeniería.','Ingeniería.'),
        ('Licenciatura.','Licenciatura'),
        ('Administrador Público.','Administrador Público')

    ]
    nombreDirector = models.CharField(max_length=50, verbose_name='Director actual de la Carrera')
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Carrera', unique = True)
    tipoTitulo = models.CharField(choices=tipoTitulos, max_length=40, verbose_name='Tipo del título a obtener', help_text='Ingeniería en Informática', default='Ingeniería')
    idFacultad = models.ForeignKey(Facultad, verbose_name='Facultad', on_delete=CASCADE)
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
    def getDirectorCarrera(self):
        return Usuarios.objects.get(pk = int(self.nombreDirector))

class Perfiles(datosAuditoria):
    nombre = models.CharField(max_length=20, verbose_name='Perfiles', unique = True)
    def __str__(self) -> str:
        return '{}'.format(self.nombre)
    def getInicial(self) -> str:
        return '{}'.format(self.nombre[0])
        
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
class Nivel(datosAuditoria):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Nivel')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
    class Meta:
        ordering = ['pk', 'nombre']
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
class Cohorte(datosAuditoria):
    meses = [(mes, mes) for mes in getMeses()]
    mesInicio = models.CharField(choices=meses, verbose_name='Mes Inicio', max_length=10)
    yearInicio = models.PositiveIntegerField(verbose_name='Año inicio')
    mesFin = models.CharField(choices=meses, verbose_name='Mes Fin', max_length=10)
    yearFin= models.PositiveIntegerField(verbose_name='Año Fin')
    cohorte = models.CharField(max_length=10, verbose_name='Nombre de Cohorte', primary_key=True)
    def __str__(self):
        return self.cohorte

class GeneracionFirmas(datosAuditoria):
    uuIDFirma = models.CharField(max_length=36, primary_key=True)
    firmaUsuario = models.ImageField(verbose_name='Firma', upload_to='usuario/firma', null = True, blank = True)
    idUsuario = models.PositiveIntegerField()
    def __str__(self):
        return Usuarios.objects.get(pk = self.idUsuario).getInformacion()

class Usuarios(AbstractUser):
    modalidades = [
        ('Trabajo de Integración Curricular','Trabajo de Integración Curricular'),
        ('Examen con Carácter Complexivo','Examen con Carácter Complexivo')
    ]
    abreviaturas = [
        ('MSc.','MSc.'),
        ('Mg.','Mg.'),
        ('Mtr.','Mtr.'),
        ('PhD.','PhD.')
    ]
    generos = [
        ('H','Hombre'),
        ('M','Mujer')
    ]
     
    imagen = models.ImageField(verbose_name='Imagen', upload_to='users', null = True, blank = True)
    perfil = models.ForeignKey(Perfiles, verbose_name='Perfil', default = 3, on_delete=CASCADE, null=True, blank=True)
    celular = models.CharField(max_length=10, verbose_name='Celular')
    modalidad = models.CharField(choices=modalidades,max_length=50, null = True, blank = True)
    idNivel = models.ForeignKey(Nivel, verbose_name='Nivel', on_delete=CASCADE, null = True, blank = True)
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE, null=True, blank=True)
    token = models.CharField(max_length=36, blank=True, null=True, editable=False)
    firma = models.ForeignKey(GeneracionFirmas, on_delete=models.SET_NULL, null=True, blank=True)
    abreviatura = models.CharField(choices=abreviaturas, max_length=8, verbose_name='Abreviatura', default='MSc.')
    genero = models.CharField(choices=generos, max_length=1, verbose_name='Genero', default='H')
    memorandoTutor = models.CharField(max_length=9,blank=True, null=True, editable=False)
    fechaMemorandoTutor = models.DateField(editable=False, null=True, blank=True)
    cohorte = models.ForeignKey(Cohorte, verbose_name='Cohorte', on_delete=CASCADE, null=True, blank=True)
    esExtranjero = models.BooleanField(default=False)
    # username = models.CharField(
    #         ('Usuario'),
    #         max_length=13,
    #         unique=True,
    #         help_text=('Se requiere al menos 10 catacteres'),
    #         validators=[ValidarCedulaUsurio(extranjero=modalidad)],
    #         # validators=[vcedula],
    #         error_messages={
    #             'unique': ("Un usuario con esta cédula ya se encuentra registrado"),
    #         },
    #     )
    def getImagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'images/defaultM.png' if self.genero == 'M' else 'images/defaultH.png')
    def __str__(self):
        return '{} {} [{}] -> {}'.format(self.first_name, self.last_name, self.username, self.perfil)
    def getInformacion(self):
        if(self.perfil.id == 3):
            return '{} {}'.format(self.first_name, self.last_name)
        else:
            return '{} {} {}'.format(self.abreviatura, self.first_name, self.last_name)
    class Meta:
        ordering = ['-perfil__nombre']

            
    def getAlias(self):
        return '{}. {}.'.format(self.first_name, self.last_name[0] if self.last_name else self.pk)
    def getNombreCompleto(self):
        return '{} {}'.format(self.last_name, self.first_name)
    def toJSON(self):
        txt = model_to_dict(self)
        if self.last_login:
            txt['last_login'] = self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        txt['date_joined'] = self.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        txt['imagen'] = self.getImagen()
        txt['firma'] = None 
        return txt
    def getGenero(self):
        if self.genero == 'M':
            return 'Señorita'
        return 'Señor'
    
    def clean(self):
        cleaned_data = super().clean()
        esExtranjero = self.esExtranjero
        if(esExtranjero is False and self.pk is None):
            ValidarCedulaUsurio(cedula=self.username)
        if self.firma is None:
            try:
                idUsuario = ((Usuarios.objects.latest('pk').id) + 1 ) if self.pk is None else self.pk
                dominioActual = Constantes.objects.get(nombre = 'DOMINIO').valor
                uuIDFirma = str(uuid.uuid4())
                nombreArchivo = f'{self.username}_{self.last_name}_{idUsuario}.png'
                firmaQR = f'**********************************'
                firmaQR += f'**********************************\n'
                firmaQR += 'SISTEMA DE INTEGRACION CURRICULAR\n'
                firmaQR += '*** FIRMADO POR ***\n'
                firmaQR += f'Cédula: {self.username}.\n'
                firmaQR += f'Nombres: {self.first_name}.\n'
                firmaQR += f'Apellidos: {self.last_name}.\n'
                firmaQR += 'Universidad Politécnica Estatal del Carchi.\n'
                firmaQR += f'{self.request.META["HTTP_HOST"]}/validarFirmaUIAP/{uuIDFirma}\n'
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
                                    idUsuario = idUsuario)
                    generarFirma.save()
                    f.close()
                    self.firma = generarFirma
                    remove(nombreArchivo)
            except Exception as e:
                print('Error al guardar el archivo generado ln-218: ', e)
            
    def save(self, *args, **kwargs):
        if self.fechaMemorandoTutor is None:
            self.fechaMemorandoTutor = timezone.now()

        if Usuarios.objects.all().count() == 0 and Perfiles.objects.all().count() == 0:
            perfil = Perfiles.objects.create(nombre = "Admin")
            perfil.save()
            perfil = Perfiles.objects.create(nombre = "Docente")
            perfil.save()
            perfil = Perfiles.objects.create(nombre = "Estudiante")
            perfil.save()
            self.perfil = Perfiles.objects.get(nombre = 'Admin')
        if self.pk is None and Usuarios.objects.all().count() > 0:
            self.set_password(self.password)
        return super().save(*args, **kwargs)
# class GrupoExperto(datosAuditoria):
#     nombre = models.CharField(max_length=40, verbose_name='Nombre del grupo', unique = True)
#     idDocentes = models.ManyToManyField(Usuarios, verbose_name='Docentes')
#     def __str__(self):
#         return self.nombre
#     def getMiembros(self):
#         ul = ''
#         for docentes in self.idDocentes.all():
#             ul += f'<li> {docentes} </li>'
#         ul = f'<ul>{ul}</ul>'
#         return ul
#     def save(self, *args, **kwargs):
#         self.setDatosAuditoria()
#         return super(self.__class__, self).save(*args, **kwargs) 

class Documento(datosAuditoria):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Documento')
    archivo = models.FileField(verbose_name='Archivo', upload_to='formatoDocumentos')
    idPerfiles = models.ManyToManyField(Perfiles, verbose_name='Disponible para', blank = True) 
    def __str__(self):
        return self.nombre
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)

class SeguimientoDocumentacion(datosAuditoria):
    opciones = [
        (False, 'Pendiente'),
        (True, 'Aprobado'),
        (None, 'Rechazado')
    ]
    idDocumento = models.ForeignKey(Documento, verbose_name='Documento', on_delete=CASCADE)
    idUsuario = models.ForeignKey(Usuarios, verbose_name='Usuario', on_delete=CASCADE)
    estado = models.BooleanField(choices=opciones,verbose_name='Estado del archivo', default=False, null = True, blank = True)   
    archivo = models.FileField(verbose_name='Documento', upload_to='documentacionEstudiante')
    def __str__(self):
        return f'{self.idUsuario}'
    def save(self, *args, **kwargs):
        self.setDatosAuditoria()
        return super(self.__class__, self).save(*args, **kwargs)
    class Meta:
        ordering = ['idUsuario__first_name']
class Constantes(datosAuditoria):
    nombre = models.CharField(max_length=10, verbose_name='* Nombre', unique = True)
    valor = models.CharField(max_length=100, verbose_name='* Valor')
    descripcion = models.TextField(max_length=200, verbose_name='Descripcion')
    def __str__(self):
        return self.nombre
