from django.db import models
from django.db.models.deletion import CASCADE
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
class Estudiante(models.Model):
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.CharField(max_length=100, verbose_name='E-mail')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    celular = models.CharField(max_length=10, verbose_name='Celular')
    foto = models.ImageField(verbose_name='Fotografía', upload_to='estudiantes', null = True, blank = True)
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0} {1}'
        return txt.format(self.nombre, self.apellido)
class ListaVerificacion(models.Model):
    detalles = [
        (1,'Solicitud de opción de titulación/Certificado de idoneidad.'),
        (2,'Oficio o correo electrónico de llamado para elaborar el cronograma.'),
        (3,'Cronograma de trabajo.')
    ]
    idEstudiante = models.ForeignKey(Estudiante, verbose_name='Estudiante', on_delete=CASCADE)
    nombreArchivo = models.PositiveIntegerField(verbose_name='Detalle', choices=detalles)
    observacion = models.TextField(max_length=100, verbose_name='Observación', null = True, blank = True)
    cumplimiento = models.BooleanField(default=False, verbose_name='Cumplimiento')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
class Docente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    email = models.CharField(max_length=100, verbose_name='E-mail')
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    celular = models.CharField(max_length=10, verbose_name='Celular')
    foto = models.ImageField(verbose_name='Fotografía', upload_to='estudiantes', null = True, blank = True)
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0} {1}'
        return txt.format(self.nombre, self.apellido)
class Nivel(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Nivel')
    periodoInicio = models.DateField( verbose_name='Periodo de inicio de Proyecto')
    periodoFin = models.DateField( verbose_name='Periodo de fin de Proyecto', null = True, blank = True)
    periodoActual = models.DateField( verbose_name='Periodo Actual')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombre)

class Proyecto(models.Model):
    idCarrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=CASCADE)
    idNivel = models.ForeignKey(Nivel, verbose_name='Nivel', on_delete=CASCADE)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Proyecto')
    idDocente = models.ForeignKey(Docente, verbose_name='Docente', on_delete=CASCADE)
    idEstudiantes = models.ManyToManyField(Estudiante, verbose_name='Listado de Estudiantes')
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
        
class Avance(models.Model):
    idProyecto = models.ForeignKey(Proyecto, verbose_name='Proyecto', on_delete=CASCADE)
    nombreAvance = models.CharField(max_length=100, verbose_name='Nombre Avance')
    observacion = models.CharField(max_length=100, verbose_name='Observacion')
    porcentaje = models.PositiveIntegerField(verbose_name='Porcentaje completado')
    def __str__(self) -> str:
        txt = '{0}'
        return txt.format(self.nombreAvance)
class Tribunal(models.Model):
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
    # primerDocente = models.ForeignKey(Docente, on_delete=CASCADE,to_field='primerDocente', verbose_name='Primer Docente')
    # segundoDocente = models.ForeignKey(Docente, on_delete=CASCADE, to_field='segundoDocente', verbose_name='Segundo Docente')
    # terceroDocente = models.ForeignKey(Docente, on_delete=CASCADE, verbose_name='Tercer Docente')
    # primerDocenteSuplente = models.ForeignKey(Docente, on_delete=CASCADE, verbose_name='Primer Docente Suplente')
    # segundoDocenteSuplente = models.ForeignKey(Docente, on_delete=CASCADE, verbose_name='Segundo Docente Suplente')
    # terceroDocenteSuplente = models.ForeignKey(Docente, on_delete=CASCADE, verbose_name='Tercer Docente Suplente')
    fechaDefensa = models.DateTimeField()
    aula = models.PositiveIntegerField(choices=aulas, verbose_name='Aula de defensa asignada')
    fechaCreacion = models.DateField(auto_now_add=True)
    fechaModificacion= models.DateField(null = True, blank = True, editable=False)
    def __str__(self) -> str:
        txt = '{0} - {1}'
        return txt.format(self.aula, self.fechaDefensa)