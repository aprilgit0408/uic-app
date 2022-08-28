from django.contrib import admin
from .models import *
# Registramos los modelos para la pantallla del administrador
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Estudiante)
admin.site.register(ListaVerificacion)
admin.site.register(Docente)
admin.site.register(Nivel)
admin.site.register(Proyecto)
admin.site.register(Avance)
admin.site.register(Tribunal)
admin.site.register(Usuarios)