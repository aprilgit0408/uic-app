from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.shortcuts import redirect, render
from App.Modules.Formularios.forms import formularioUsuarios
from App.models import Carrera, GrupoExperto, Usuarios
from uicApp.settings import LOGIN_REDIRECT_URL
modelo = Usuarios
formulario = formularioUsuarios
entidad = 'Registro'
main = 'main.html'
url = reverse_lazy('app:grupoExpertos')
class Login(LoginView):
    template_name = 'Login/index.html'
    success_url = reverse_lazy('dashboard')
    mensaje = 'Si los datos son correctos, le eviaremos un correo al Email ingresado. \n'
    mensaje += 'Por favor, revise la bandeja de entrada.'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.mensaje = ''
        return super().post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cont = self.request.GET.__contains__('forget')
        if cont:
            context['mensaje'] = self.mensaje
        context['title'] = f'Ingreso al Sistema'
        return context
class addUser (CreateView):
    model = modelo
    form_class = formulario
    template_name = 'Login/registro.html'
    success_url = url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['carreras'] = Carrera.objects.all()
        return context