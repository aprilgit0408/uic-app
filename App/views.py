from django.views.generic.base import TemplateView
from App.Modules.Formularios.forms import formularioPerfilUsuario
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import  UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from Usuarios.models import Usuarios

entidad = 'Usuario'
main = 'main.html'
formulario = formularioPerfilUsuario
class Index(TemplateView):
    template_name = "index.html"
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class PerfilUsuario(LoginRequiredMixin, UpdateView):
    model = Usuarios
    form_class = formulario
    template_name = main
    success_url = '/login'
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    def get_object(self, queryset = None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = formulario(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['accion'] = f'Edición de {entidad}'
        return context
class editProfilePasswords(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    success_url = '/login/'
    template_name = 'password.html'
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contraseña'
        context['ruta'] = self.success_url
        return context