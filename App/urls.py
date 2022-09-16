from django.urls import path
from App.Modules.Documentos.view import GuardarDocumento, addDocumentos, generarPDF, listarDocumentos
from App.Modules.Facultades.view import listarFacultades, addFacultades, editFacultades, deleteFacultades
from App.Modules.Carreras.view import listarCarreras, addCarreras, editCarreras, deleteCarreras
from App.Modules.GrupoExperto.view import addGrupoExpertos, deleteGrupoExpertos, editGrupoExpertos, listarGrupoExpertos
from App.Modules.Login.views import Login, LogoutView, addUser, resetPassword, resetPasswordLink
from App.Modules.Tutorias.view import addTutorias, deleteTutorias, editTutorias, listarTutorias
from App.Modules.Verificacion.view import listarListaVerificaciones, addListaVerificaciones, editListaVerificaciones, deleteListaVerificaciones
from App.Modules.Proyectos.view import listarDocentes, listarEstudiantes, listarProyectos, addProyectos, editProyectos, deleteProyectos

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

    #Grupo de expertos
    path('app/grupoExpertos/',  listarGrupoExpertos.as_view(), name='grupoExpertos'),
    path('app/grupoExpertos/add',  addGrupoExpertos.as_view(), name='addGrupoExpertos'),
    path('app/grupoExpertos/edit/<pk>',  editGrupoExpertos.as_view(), name='editGrupoExpertos'),
    path('app/grupoExpertos/delete/<pk>',  deleteGrupoExpertos.as_view(), name='deleteGrupoExpertos'),
    
    path('app/estudiantes/',  listarEstudiantes.as_view(), name='estudiantes'),
    path('app/docentes/',  listarDocentes.as_view(), name='docentes'),
    path('app/documentos/',  listarDocumentos.as_view(), name='documentos'),
    path('app/documentos/add',  addDocumentos.as_view(), name='addDocumentos'),
    path('app/documentos/generar/<pk>',  generarPDF.as_view(), name='generarPDF'),
    path('app/documentos/enviar/<pk>',  GuardarDocumento.as_view(), name='guardarDocumento'),
    
    path('app/tutorias/',  listarTutorias.as_view(), name='tutorias'),
    path('app/tutorias/add',  addTutorias.as_view(), name='addTutorias'),
    path('app/tutorias/edit/<int:pk>',  editTutorias.as_view(), name='editTutorias'),
    path('app/tutorias/delete/<int:pk>',  deleteTutorias.as_view(), name='deleteTutorias'),
    
    
    path('',  Index.as_view(), name='index'),
    path('login/',  Login.as_view(), name='login'),
    path('login/add',  addUser.as_view(), name='agregarUsuario'),
    path('login/reset',  resetPassword.as_view(), name='reset'),
    path('login/password/<str:token>',resetPasswordLink.as_view(), name='resetPassword'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('index',  Index.as_view(), name='index')
]