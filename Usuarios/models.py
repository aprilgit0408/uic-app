from distutils.command.upload import upload
from django.db import models
from django.db.models.deletion import CASCADE
from uicApp.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth.models import AbstractUser

class Facultad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Facultad', primary_key=True)
    sigla = models.CharField(max_length=20, verbose_name='Nombre corto')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        return self.nombre

class Carrera(models.Model):
    generos = [
        ('Señor','Señor'),
        ('Señora','Señora')
    ]
    abreviaturas = [
        ('MSc.','MSc.'),
        ('Mg.','Mg.'),
        ('Mtr.','Mtr.'),
        ('PhD.','PhD.')
    ]
    genero = models.CharField(choices=generos, max_length=10, verbose_name='Seleccione')
    abreviatura = models.CharField(choices=abreviaturas, max_length=8, verbose_name='Abreviatura')
    nombreDirector = models.CharField(max_length=50, verbose_name='Director actual de la Carrera')
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
class Nivel(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Nivel')
    periodoInicio = models.DateField( verbose_name='Periodo de inicio de Proyecto')
    periodoFin = models.DateField( verbose_name='Periodo de fin de Proyecto', null = True, blank = True)
    periodoActual = models.DateField( verbose_name='Periodo Actual')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)
def vcedula(texto):
    nocero = texto.strip("0")
    cedula = int(nocero,0)
    verificador = cedula%10
    numero = cedula//10
    suma = 0
    while (numero > 0):
        posimpar = numero%10
        numero   = numero//10
        posimpar = 2*posimpar
        if (posimpar  > 9):
            posimpar = posimpar-9
        pospar = numero%10
        numero = numero//10
        suma = suma + posimpar + pospar
    decenasup = suma//10 + 1
    calculado = decenasup*10 - suma
    if (calculado  >= 10):
        calculado = calculado - 10
    if (calculado == verificador):
        return texto
    else:
        raise ValidationError("La cédula ingresada no es válida") 
     

class Usuarios(AbstractUser):
    modalidades = [
        ('Trabajo de Integración Curricular','Trabajo de Integración Curricular'),
        ('Examen con Carácter Complexivo','Examen con Carácter Complexivo')
    ]
     
    imagen = models.ImageField(verbose_name='Imagen', upload_to='users', null = True, blank = True)
    perfil = models.ForeignKey(Perfiles, verbose_name='Perfil', on_delete=CASCADE, null=True, blank=True)
    celular = models.CharField(max_length=10, verbose_name='Celular')
    modalidad = models.CharField(choices=modalidades,max_length=50, null = True, blank = True)
    idNivel = models.ForeignKey(Nivel, verbose_name='Nivel', on_delete=CASCADE, null = True, blank = True)
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE, null=True, blank=True)
    token = models.CharField(max_length=36, blank=True, null=True, editable=False)
    firma = models.ImageField(verbose_name='Firma', upload_to='usuario/firma', null = True, blank = True)
    def getImagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'images/default.jpg')
    def __str__(self):
        return '{} {} [{}]'.format(self.first_name, self.last_name, self.username)
    def getInformacion(self):
        return '{} {}'.format(self.first_name, self.last_name)
    def getAlias(self):
        return '{}. {}'.format(self.first_name, self.last_name[0])
    def clean(self):
        super().clean()
    def save(self, *args, **kwargs):
        if Usuarios.objects.all().count() == 0:
            perfil = Perfiles.objects.create(nombre = "Admin")
            perfil.save()
            perfil = Perfiles.objects.create(nombre = "Docente")
            perfil.save()
            perfil = Perfiles.objects.create(nombre = "Estudiante")
            perfil.save()
            self.perfil = Perfiles.objects.get(nombre = 'Admin')
        if self.pk is None:
            self.set_password(self.password)
        return super().save(*args, **kwargs)
        
