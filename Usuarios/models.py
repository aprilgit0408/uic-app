from django.db import models
from django.db.models.deletion import CASCADE
from uicApp.settings import MEDIA_URL, STATIC_URL
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError 

class Facultad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de la Facultad', primary_key=True)
    sigla = models.CharField(max_length=20, verbose_name='Nombre corto')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        return self.nombre

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
    @deconstructible
    class UnicodeUsernameValidator(validators.RegexValidator):
        regex = r'^[\w.@+-]+\Z'
        message = (
            'Enter a valid username. This value may contain only letters, '
            'numbers, and @/./+/-/_ characters.'
        )
        flags = 0
    modalidades = [
        ('1','Trabajo de Integración Curricular (TIC)'),
        ('2','Examen con Carácter Complexivo (ECC)')
    ]
          
    imagen = models.ImageField(verbose_name='Imagen', upload_to='users', null = True, blank = True)
    perfil = models.ForeignKey(Perfiles, verbose_name='Perfil', default='Estudiante', on_delete=CASCADE, null=True, blank=True)
    celular = models.CharField(max_length=10, verbose_name='Celular')
    modalidad = models.CharField(choices=modalidades,max_length=1, null = True, blank = True)
    username_validator = UnicodeUsernameValidator
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE, null=True, blank=True)
    token = models.CharField(max_length=36, blank=True, null=True, editable=False)
    username = models.CharField(
        ('Usuario'),
        max_length=13,
        unique=True,
        help_text=('Se requiere al menos 10 catacteres'),
        # validators=[vcedula],
        error_messages={
            'unique': ("Un usuario con esta cédula ya se encuentra registrado"),
        },
    )   
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
        if self.pk is None:
            self.set_password(self.password)
        return super().save(*args, **kwargs)
        
