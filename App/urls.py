from django.urls import path
from App.Modules.Avances.view import addAvances, deleteAvances, editAvances, guardarAvance, guardarAvanceEstudiante, listarAvances
from App.Modules.Documentos.view import GuardarDocumento, guardarSolicitud, listadoSolicitudes, addDocumentos, generarPDF, listarDocumentos
from App.Modules.Facultades.view import listarFacultades, addFacultades, editFacultades, deleteFacultades
from App.Modules.Carreras.view import listarCarreras, addCarreras, editCarreras, deleteCarreras
from App.Modules.Login.views import Login, LogoutView, addUser, resetPassword, resetPasswordLink
from App.Modules.Reportes.view import getReportes
from App.Modules.Tribunal.view import addTribunal, deleteTribunal, editTribunal, listarTribunal
from App.Modules.Tutorias.view import addTutorias, deleteTutorias, editTutorias, listarTutorias
from App.Modules.Verificacion.view import guardarListaVerificacion, listarListaVerificaciones, addListaVerificaciones, editListaVerificaciones, deleteListaVerificaciones
from App.Modules.Proyectos.view import addDocente, addEstudiantes, generarPDFProyecto, guardarDocumento, listarDocentes, listarEstudiantes, listarProyectos, addProyectos, editProyectos, deleteProyectos

from App.views import Index, PerfilUsuario, editProfilePasswords
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
    path('app/listaVerificaciones/guardar/<int:pk>',  guardarListaVerificacion.as_view(), name='guardarListaVerificacion'),

    
    # Serivicio Para los Proyectos
    path('app/proyectos/',  listarProyectos.as_view(), name='proyectos'),
    path('app/proyectos/add',  addProyectos.as_view(), name='addProyectos'),
    path('app/proyectos/edit/<int:pk>',  editProyectos.as_view(), name='editProyectos'),
    path('app/proyectos/delete/<int:pk>',  deleteProyectos.as_view(), name='deleteProyectos'),
    path('app/proyectos/pdf',  generarPDFProyecto.as_view(), name='gererarPDFTEST'),
    path('app/proyectos/guardar',  guardarDocumento.as_view(), name='guardarDocumento'),


    # Serivicio Para los Avances
    path('app/avances/',  listarAvances.as_view(), name='avances'),
    path('app/avances/save/<int:pk>',  guardarAvance.as_view(), name='guardarAvances'),
    path('app/avances/guardar/<int:pk>',  guardarAvanceEstudiante.as_view(), name='guardarAvancesEstudiante'),
    path('app/avances/add',  addAvances.as_view(), name='addAvances'),
    path('app/avances/edit/<int:pk>',  editAvances.as_view(), name='editAvances'),
    path('app/avances/delete/<int:pk>',  deleteAvances.as_view(), name='deleteAvances'),

    #Grupo de expertos
    # path('app/grupoExpertos/',  listarGrupoExpertos.as_view(), name='grupoExpertos'),
    # path('app/grupoExpertos/add',  addGrupoExpertos.as_view(), name='addGrupoExpertos'),
    # path('app/grupoExpertos/edit/<pk>',  editGrupoExpertos.as_view(), name='editGrupoExpertos'),
    # path('app/grupoExpertos/delete/<pk>',  deleteGrupoExpertos.as_view(), name='deleteGrupoExpertos'),
    
    path('app/estudiantes/',  listarEstudiantes.as_view(), name='estudiantes'),
    path('app/estudiantes/add',  addEstudiantes.as_view(), name='addEstudiantes'),
    path('app/docentes/',  listarDocentes.as_view(), name='docentes'),
    path('app/docentes/add',  addDocente.as_view(), name='addDocentes'),
    
    #vista para documentos
    path('app/documentos/',  listarDocumentos.as_view(), name='documentos'),
    path('app/documentos/solicitudes/',  listadoSolicitudes.as_view(), name='solicitudes'),
    path('app/documentos/solicitudes/guardar',  guardarSolicitud.as_view(), name='guardarSolicitud'),
    path('app/documentos/add',  addDocumentos.as_view(), name='addDocumentos'),
    path('app/documentos/generar/<pk>',  generarPDF.as_view(), name='generarPDF'),
    path('app/documentos/enviar/<pk>',  GuardarDocumento.as_view(), name='guardarDocumento'),

   #Turias 
    path('app/tutorias/',  listarTutorias.as_view(), name='tutorias'),
    path('app/tutorias/add',  addTutorias.as_view(), name='addTutorias'),
    path('app/tutorias/edit/<int:pk>',  editTutorias.as_view(), name='editTutorias'),
    path('app/tutorias/delete/<int:pk>',  deleteTutorias.as_view(), name='deleteTutorias'),
    
    #Tribunal
    path('app/tribunal/',  listarTribunal.as_view(), name='tribunal'),
    path('app/tribunal/add',  addTribunal.as_view(), name='addTribunal'),
    path('app/tribunal/edit/<int:pk>',  editTribunal.as_view(), name='editTribunal'),
    path('app/tribunal/delete/<int:pk>',  deleteTribunal.as_view(), name='deleteTribunal'),
    
    #Reportes
    path('app/reportes/',  getReportes.as_view(), name='reportes'),
    

    
    path('',  Index.as_view(), name='index'),
    path('login/',  Login.as_view(), name='login'),
    path('login/add',  addUser.as_view(), name='agregarUsuario'),
    path('login/reset',  resetPassword.as_view(), name='reset'),
    path('login/password/<str:token>',resetPasswordLink.as_view(), name='resetPassword'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('perfil/',  PerfilUsuario.as_view(), name='perfil'),
    path('perfil/password',  editProfilePasswords.as_view(), name='editPassword'),
    path('index',  Index.as_view(), name='index')
]