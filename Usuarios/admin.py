from django.contrib import admin
from .models import Carrera, Facultad, Perfiles, Usuarios
# Register your models here.
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Perfiles)
admin.site.register(Usuarios)
