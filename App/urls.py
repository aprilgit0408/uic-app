from django.urls import path

from App.Modules.Facultades.view import listarFacultades, addFacultades, editFacultades, deleteFacultades
from App.Modules.Carreras.view import listarCarreras, addCarreras, editCarreras, deleteCarreras
from App.Modules.Verificacion.view import listarListaVerificaciones, addListaVerificaciones, editListaVerificaciones, deleteListaVerificaciones
from App.Modules.Proyectos.view import listarProyectos, addProyectos, editProyectos, deleteProyectos
from App.Modules.Docentes.view import listarDocentes, addDocentes, editDocentes, deleteDocentes
from App.Modules.Estudiantes.view import listarEstudiantes, addEstudiantes, editEstudiantes, deleteEstudiantes

from App.views import Index
app_name = 'app'
urlpatterns = [
    # Serivicio Para las Facultades
    path('app/facultades/',  listarFacultades.as_view(), name='facultades'),
    path('app/facultades/add',  addFacultades.as_view(), name='addFacultades'),
    path('app/facultades/edit/<pk>',  editFacultades.as_view(), name='editFacultades'),
    path('app/facultades/delete/<pk>',  deleteFacultades.as_view(), name='deleteFacultades'),
    
    # Serivicio Para las Carreras
    path('app/carreras/',  listarCarreras.as_view(), name='carreras'),
    path('app/carreras/add',  addCarreras.as_view(), name='addCarreras'),
    path('app/carreras/edit/<pk>',  editCarreras.as_view(), name='editCarreras'),
    path('app/carreras/delete/<pk>',  deleteCarreras.as_view(), name='deleteCarreras'),
    
    # Serivicio Para las ListaVerificaciones
    path('app/listaVerificaciones/',  listarListaVerificaciones.as_view(), name='listaVerificaciones'),
    path('app/listaVerificaciones/add',  addListaVerificaciones.as_view(), name='addListaVerificaciones'),
    path('app/listaVerificaciones/edit/<pk>',  editListaVerificaciones.as_view(), name='editListaVerificaciones'),
    path('app/listaVerificaciones/delete/<pk>',  deleteListaVerificaciones.as_view(), name='deleteListaVerificaciones'),
    
    # Serivicio Para los Proyectos
    path('app/proyectos/',  listarProyectos.as_view(), name='proyectos'),
    path('app/proyectos/add',  addProyectos.as_view(), name='addProyectos'),
    path('app/proyectos/edit/<int:pk>',  editProyectos.as_view(), name='editProyectos'),
    path('app/proyectos/delete/<int:pk>',  deleteProyectos.as_view(), name='deleteProyectos'),
    
    # Serivicio Para los Docentes
    path('app/docentes/',  listarDocentes.as_view(), name='docentes'),
    path('app/docentes/add',  addDocentes.as_view(), name='addDocentes'),
    path('app/docentes/edit/<int:pk>',  editDocentes.as_view(), name='editDocentes'),
    path('app/docentes/delete/<int:pk>',  deleteDocentes.as_view(), name='deleteDocentes'),
    
    # Serivicio Para los Estudiantes
    path('app/estudiantes/',  listarEstudiantes.as_view(), name='estudiantes'),
    path('app/estudiantes/add',  addEstudiantes.as_view(), name='addEstudiantes'),
    path('app/estudiantes/edit/<int:pk>',  editEstudiantes.as_view(), name='editEstudiantes'),
    path('app/estudiantes/delete/<int:pk>',  deleteEstudiantes.as_view(), name='deleteEstudiantes'),
    
    
    
    path('',  Index.as_view(), name='index'),
    path('index',  Index.as_view(), name='index')
]