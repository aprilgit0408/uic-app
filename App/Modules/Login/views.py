from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.views import LoginView, LogoutView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.shortcuts import redirect, render
from App.Modules.Formularios.forms import formularioUsuarios, resetPasswordForm, resetPasswordFormLink
from App.models import Carrera, Usuarios
from uicApp.settings import LOGIN_REDIRECT_URL, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DOMAIN
import uuid
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


class addUser(CreateView):
    model = modelo
    form_class = formulario
    template_name = 'Login/registro.html'
    success_url = url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{entidad}'
        context['carreras'] = Carrera.objects.all()
        return context


class resetPassword(FormView):
    form_class = resetPasswordForm
    template_name = 'Login/reset.html'
    success_url = '/login/'
    mensaje = 'Si los datos son correctos, le eviaremos un correo al Email ingresado. \n'
    mensaje += 'Por favor, revise su bandeja de entrada.'
    def send_mail(self, id, mail):
        try:
            Subject = 'Reseteo de Contraseña'
            password = str(uuid.uuid4())

            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = mail
            mensaje['Subject'] = Subject
            
            mailServer = SMTP(EMAIL_HOST, port=EMAIL_PORT)
            print(mailServer.ehlo())
            mailServer.starttls()
            print(mailServer.ehlo())
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            content = render_to_string('Login/email.html',
                                       {'user': Usuarios.objects.get(pk=id), 'password': password, 'dominio': DOMAIN})
            mensaje.attach(MIMEText(content, 'html'))
            mailServer.sendmail(EMAIL_HOST_USER, mail, mensaje.as_string())
            update = Usuarios.objects.get(pk=id)
            update.token = password
            update.save()
            mailServer.quit()
        except Exception as e:
            print('Error Email l-86', e)

    def post(self, request, *args, **kwargs):
        try:
            username = request.POST['username']
            email = request.POST['email']
            usuario = Usuarios.objects.get(username=username)
            if usuario.email == email:
                self.send_mail(usuario.pk, email)
            # self.form_class.errors = self.mensaje
            return redirect('/login/?forget')
        except Exception as e:
            print('Error: Reset ln-104:  ', e)
            self.form_class.errors = self.mensaje
            return redirect('/login/?forget')

class resetPasswordLink(FormView):
    user = ''
    form_class = resetPasswordFormLink
    template_name = 'Login/resetlink.html'

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if Usuarios.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return redirect('/login/')

    def post(self, request, *args, **kwargs):
        try:
            token = self.kwargs['token']
            user = Usuarios.objects.get(token=token)
            p1 = request.POST['password1']
            p2 = request.POST['password2']
            if len(token) == 36:
                if p1 == p2:
                    user = Usuarios.objects.get(pk=user.id)
                    user.set_password(p2)
                    user.token = ''
                    user.save()
                    return redirect('/login/')
                else:
                    return render(request, 'Login/resetlink.html',
                                  {'mensaje_error': 'Las contraseñas no coinciden, por favor, ingrese nuevamente'})
            return render(request, 'Login/resetlink.html', {'mensaje_error': 'Por favor, verifique que el link sea correcto'})
        except Exception as e:
            print('Error ln-151: ResetPassword', e)
            return render(request, 'Login/resetlink.html', {'mensaje_error': 'Por favor, verifique que el link sea correcto'})
