from django.contrib import admin
from .models import Carrera, Constantes, Documento, Facultad, GrupoExperto, Nivel, Perfiles, SeguimientoDocumentacion, Usuarios
# Register your models here.
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Perfiles)
admin.site.register(Usuarios)
admin.site.register(Documento)
admin.site.register(SeguimientoDocumentacion)
admin.site.register(GrupoExperto)
admin.site.register(Constantes)
admin.site.register(Nivel)
 