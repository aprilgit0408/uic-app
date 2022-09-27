from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Usuarios.models import Usuarios
from uicApp.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
import uuid
def send_mail(asunto, destinatarios, content):
        '''
        content = render_to_string('Login/email.html',
                                        {'user': usuario, 'password': password, 'dominio': DOMAIN})
        '''
        try:
            mensaje = MIMEMultipart()
            mensaje['From'] = EMAIL_HOST_USER
            mensaje['To'] = destinatarios
            mensaje['Subject'] = asunto
            
            mailServer = SMTP(EMAIL_HOST, port=EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            mensaje.attach(MIMEText(content, 'html'))
            mailServer.sendmail(EMAIL_HOST_USER, destinatarios.split(','), mensaje.as_string())
            print('Mails enviados a: ', destinatarios)
            mailServer.quit()
        except Exception as e:
            print('Error Email l-25', e)
        return True
def send_mail_Reset(id, mail, content):
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
            mensaje.attach(MIMEText(content, 'html'))
            mailServer.sendmail(EMAIL_HOST_USER, mail, mensaje.as_string())
            update = Usuarios.objects.get(pk=id)
            update.token = password
            update.save()
            mailServer.quit()
        except Exception as e:
            print('Error Email l-46', e)
def getDate(fecha):
    '''
    @param fecha para transformar
    @return Vie 23 Sep del 2022
    '''
    meses = [None, "Ene", "Feb", "Mar", "Abr", "May", "Jun",
                        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    dias = [None, "Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
    dia = fecha.toordinal() % 7 or 7
    fechaActual = dias[dia] + ', ' + str(fecha.day) + ' ' +  meses[fecha.month] + ' del ' + str(fecha.year) + ' ' + fecha.strftime("%H:%M:%S")
    return fechaActual