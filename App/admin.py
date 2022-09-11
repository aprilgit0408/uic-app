from django.contrib import admin
from .models import Avance,GrupoExperto, Imagenes, Informacion, ListaVerificacion, Nivel, Proyecto, Tribunal, Tutoria
# # Registramos los modelos para la pantallla del administrador
admin.site.register(ListaVerificacion)
admin.site.register(Nivel)
admin.site.register(Proyecto)
admin.site.register(Avance)
admin.site.register(Tribunal)
admin.site.register(Imagenes)
admin.site.register(Informacion)
admin.site.register(Tutoria)
admin.site.register(GrupoExperto)