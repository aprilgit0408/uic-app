from django.contrib import admin
from .models import Avance, DocentesSuplente,ListaVerificacion, NombreArchivoListaVerificacion, Proyecto, Tribunal, Tutoria
# # Registramos los modelos para la pantallla del administrador
admin.site.register(ListaVerificacion)
admin.site.register(Proyecto)
admin.site.register(Avance)
admin.site.register(Tribunal)
admin.site.register(Tutoria)
admin.site.register(DocentesSuplente)
admin.site.register(NombreArchivoListaVerificacion)