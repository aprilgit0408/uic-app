from django.urls import path

from App.Modules.Admin.view import listarProyectos, addProyectos, editProyectos, deleteProyectos
from App.views import Index
app_name = 'app'
urlpatterns = [
    path('app/proyectos/',  listarProyectos.as_view(), name='proyectos'),
    path('app/proyectos/add',  addProyectos.as_view(), name='addProyectos'),
    path('app/proyectos/edit/<int:pk>',  editProyectos.as_view(), name='editProyectos'),
    path('app/proyectos/delete/<int:pk>',  deleteProyectos.as_view(), name='deleteProyectos'),
    path('',  Index.as_view(), name='index'),
    path('index',  Index.as_view(), name='index')
]