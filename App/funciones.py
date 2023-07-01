from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Usuarios.models import Constantes, Usuarios
from uicApp import settings
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http.response import HttpResponse
from django.shortcuts import redirect
from email.mime.base import MIMEBase
from email.message import EmailMessage
from django.utils.dateparse import parse_datetime
from backports.zoneinfo import ZoneInfo
from email import encoders
from os import remove
import os
import uuid
import datetime
import threading

def send_mail(asunto, destinatarios, content, archivo = None):
        def sendMailHilos():
            '''
            content = render_to_string('Login/email.html',
                                            {'user': usuario, 'password': password, 'dominio': DOMAIN})
            '''
            print('Inicio de envío mail a los siguientes destinatarios: ', destinatarios)
            try:
                USER_MAIL = getConstante('USER_MAIL')
                mensaje = MIMEMultipart()
                mensaje['From'] = USER_MAIL
                mensaje['To'] = destinatarios
                mensaje['Subject'] = asunto
                
                mailServer = SMTP(getConstante('EMAIL_HOST'), port=getConstante('EMAIL_PORT'))
                mailServer.starttls()
                mailServer.login(USER_MAIL, getConstante('USER_PASS'))
                mensaje.attach(MIMEText(content, 'html'))
                if(archivo):
                    with open(archivo['ruta'], "rb") as f:
                        adjunto_MIME = MIMEBase('application', 'pdf')
                        nombre_adjunto = archivo["nombreArchivo"]
                        adjunto_MIME.set_payload(f.read())
                        encoders.encode_base64(adjunto_MIME) 
                        adjunto_MIME.add_header('Content-Disposition', f'attachment; filename={nombre_adjunto}')
                        mensaje.attach(adjunto_MIME)
                
                mailServer.sendmail(USER_MAIL, destinatarios.split(','), mensaje.as_string())
                print('Mails enviados a: ', destinatarios)
                mailServer.quit()
                if(archivo):
                    remove(archivo['ruta'])
            except Exception as e:
                if(archivo):
                    remove(archivo['ruta'])
                print('Error Email l-53', e)
            return True
        hilo = threading.Thread(name='Send Mail', target=sendMailHilos)
        hilo.start()
def send_mail_Reset(id, mail, content):
        try:
            Subject = 'Reseteo de Contraseña'
            password = str(uuid.uuid4())
            USER_MAIL = getConstante('USER_MAIL')

            mensaje = MIMEMultipart()
            mensaje['From'] = USER_MAIL
            mensaje['To'] = mail
            mensaje['Subject'] = Subject
            
            mailServer = SMTP(getConstante('EMAIL_HOST'), port=getConstante('EMAIL_PORT'))
            print(mailServer.ehlo())
            mailServer.starttls()
            print(mailServer.ehlo())
            mailServer.login(USER_MAIL, getConstante('USER_PASS'))
            mensaje.attach(MIMEText(content, 'html'))
            mailServer.sendmail(USER_MAIL, mail, mensaje.as_string())
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
def getConstante(nombre):
    try:
        return Constantes.objects.get(nombre = nombre).valor
    except Exception as e:
        print('No se ha econtrado el valor para : ', nombre)
def getMeses(mes):
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    return meses[mes]

'''
Recibe parametrod de
nombreArchivo, nombreTemplateArchivo, request, urlRetorno
y retorna la respuerta http
'''
def funcionGenerarPDF(nombreArchivo, nombreTemplateArchivo, request, urlRetorno, datosAdicionales, enviarMail = None):
    response = None
    try:
        ruta = f'media/documentacionEstudiante/{request.user.getInformacion()}-{nombreArchivo}.pdf'
        result_file = open(ruta, "w+b")
        usuario = Usuarios.objects.get(pk = request.user.pk)
        data = {
            'usuario': usuario,
            'datosAdicionales': datosAdicionales,
            'nombreDocumento': nombreArchivo,
            'fecha': datetime.datetime.now().date(),
            'encabezado' : f'{settings.STATIC_URL}images/encabezado.jpg',
            'imagenCentro' : f'{settings.STATIC_URL}images/imagenCentro.jpg',
            'piePagina' : f'{settings.STATIC_URL}images/piePagina.jpg'
        }
        template = get_template(f'Documentos/{nombreTemplateArchivo}.html')
        html = template.render(data)
        css_url = os.path.join(settings.BASE_DIR, 'static/css/bootstrap.min.css')
        pdf = HTML(string=html, base_url='').write_pdf(stylesheets=[CSS(css_url)])
        rutaPDF =  os.path.join(settings.BASE_DIR, 'media/documentacion') 
        if os.path.exists(rutaPDF) and enviarMail:
            idArchivo = str(uuid.uuid4())
            nombreArchivoPDF = f'{idArchivo}.pdf'
            f = open(os.path.join(rutaPDF, nombreArchivoPDF), 'wb')
            f.write(pdf)
            f.close()
            if(enviarMail):
                archivo = {}
                archivo['nombreArchivo'] = f'{nombreArchivo}.pdf'
                archivo['ruta'] = f'{rutaPDF}/{nombreArchivoPDF}'
                send_mail(enviarMail['asunto'], enviarMail['destinatarios'], enviarMail['content'], archivo)
        result_file.close()
        response = HttpResponse(pdf, content_type='application/pdf')
    except Exception as e:
        print('Error al generar PDF ln-141: ', e)
        response = redirect(urlRetorno)
    return response

def funcionGuardarPDF(pdf,ruta, nombreArchivo):
    if os.path.exists(ruta):
        f = open(os.path.join(ruta, f'{nombreArchivo}.pdf'), 'wb')
        f.write(pdf)

def getFecha(fecha):
    parseFecha = parse_datetime(fecha)
    return parseFecha.replace(tzinfo=ZoneInfo("America/Guayaquil"))