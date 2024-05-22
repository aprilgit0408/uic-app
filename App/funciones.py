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
from PDFNetPython3.PDFNetPython import *
from typing import Tuple
import OpenSSL
import time
import os
import uuid
import datetime
import threading
rutaArchivosStaticos = './static/'
rutaArchivosMedia = './media/'
rutaCertificado = f'{rutaArchivosStaticos}certificado/'
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
                # if(archivo):
                #     remove(archivo['ruta'])
            except Exception as e:
                # if(archivo):
                #     remove(archivo['ruta'])
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

"""
Firma un documento PDF
ficheroPDFEntrada : ruta del documento a firmar
idFirma: nombre de la firma
coordenadaX : posicion en donde se pondra el codigoQR o imagen
coordenadaY : posicion en donde se pondra el codigoQR o imagen
imagenFirma: ruta de la imagen QR
paginas: None (Ya que es un solo documento)
ficheroPDFFirmado: ruta del archivo salida al momento de firmar
"""
def FirmarPDF(ficheroPDFEntrada: str, idFirma: str, coordenadaX: int, 
            coordenadaY: int, imagenFirma: str, paginas: Tuple = None, ficheroPDFFirmado: str = None):
    GenerarCertificado()   
    # An output file is automatically generated with the word signed added at its end
    if not ficheroPDFFirmado:
        ficheroPDFFirmado = (os.path.splitext(ficheroPDFEntrada)[0]) + "_firmado.pdf"
    # Inicializamos la librería de edición de ficheros PDF
    # Introducimos la clave de licencia como parámetro
    PDFNet.Initialize("demo:1638008198625:7b6e5d3b030000000000ad6c0848ed2c55e035c1937ec70d40b850090b")
    doc = PDFDoc(ficheroPDFEntrada)
    # Creamos un campo de firma (imagen de firma escaneada)
    campoFirma = SignatureWidget.Create(doc, Rect(
        coordenadaX, coordenadaY, coordenadaX + 100, coordenadaY + 50), idFirma)
    # Recorremos las páginas indicadas para agregar la firma (en imagen)
    for pagina in range(1, (doc.GetPageCount() + 1)):
        if paginas:
            if str(pagina) not in paginas:
                continue
        pg = doc.GetPage(pagina)
        # Agrega el campo de firma en la página
        pg.AnnotPushBack(campoFirma)
    # Fichero con la imagen de la firma escaneada
    imagenFirma = f'{os.path.dirname(os.path.abspath(__name__))}{imagenFirma}'
    # Fichero PFX del certificado autofirmado
    ficheroPFX = f'{rutaCertificado}container.pfx'
    # Recupera el campo de firma
    campoAprobacion = doc.GetField(idFirma)
    campoAprobacionFirma = DigitalSignatureField(campoAprobacion)
    # Agregamos la apariencia al campo de imagen de firma escaneada
    img = Image.Create(doc.GetSDFDoc(), imagenFirma)
    widgetAprobacionFirmaEncontrado  = SignatureWidget(campoAprobacion.GetSDFObj())
    widgetAprobacionFirmaEncontrado.CreateSignatureAppearance(img)
    # Preparamos la firma y el controlador de firma para firmar el documento PDF
    # print (ficheroPFX)
    campoAprobacionFirma.SignOnNextSave(ficheroPFX, '')
    # La firma se realizará durante la siguiente operación de guardado incremental
    doc.Save(ficheroPDFFirmado, SDFDoc.e_incremental)
    # Anotamos las acciones en el resumen
    resumenAcciones = {
        "PDF original": ficheroPDFEntrada, "ID de firma": idFirma, 
        "PDF firmado": ficheroPDFFirmado, "Fichero de firma": imagenFirma, 
        "Fichero de certificado": ficheroPFX
    }
    # Mostramos el resumen de acciones
    print("*******************")
    print("\n".join("{}:{}".format(i, j) for i, j in resumenAcciones.items()))
    print("*******************")
    return True


'''
Recibe parametrod de
nombreArchivo, nombreTemplateArchivo, request, urlRetorno
y retorna la respuerta http
'''
def funcionGenerarPDF(nombreArchivo, nombreTemplateArchivo, request, urlRetorno, datosAdicionales, ejeX:int, ejeY:int, url_firma:str,enviarMail = None):
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
            #se realiza firma de archivo
            rutaArchivoPDF = f'{rutaPDF}/{nombreArchivoPDF}'
            if(ejeX and ejeY):
                FirmarPDF(rutaArchivoPDF, 'UUIAPP', ejeX, ejeY,url_firma, None, rutaArchivoPDF)
            if(enviarMail):
                archivo = {}
                archivo['nombreArchivo'] = f'{nombreArchivo}.pdf'
                archivo['ruta'] = rutaArchivoPDF
                send_mail(enviarMail['asunto'], enviarMail['destinatarios'], enviarMail['content'], archivo)
                datosAdicionales['archivo']  = archivo
        result_file.close()
        response = HttpResponse(pdf, content_type='application/pdf')
    except Exception as e:
        print('Error al generar PDF ln-145: ', e)
        response = redirect(urlRetorno)
    return response

def funcionGuardarPDF(pdf,ruta, nombreArchivo):
    if os.path.exists(ruta):
        f = open(os.path.join(ruta, f'{nombreArchivo}.pdf'), 'wb')
        f.write(pdf)

def getFecha(fecha):
    parseFecha = parse_datetime(fecha)
    return parseFecha.replace(tzinfo=ZoneInfo("America/Guayaquil"))

def idsListaVerificacionObl():
    return {1: 'a', 3:'b',33:'c',14:'d', 16:'e',17:'f'}
def getAbecedario():
    return ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']



"""
Para crear un certificado autofirmado.
Este certificado no requiere la firma de una autoridad de certificación externa.
"""
def CrearCertificadoAutofirmado(parDeClaves):
    # Crea un certificado autofirmado
    certificado = OpenSSL.crypto.X509()
    # Nombre Común para el certificado
    # Este dato aparecerá en el Emisor del certificado
    certificado.get_subject().C = "EC"
    certificado.get_subject().ST = "Carchi"
    certificado.get_subject().L = "Tulcán"
    certificado.get_subject().O = "Universidad Politécnica Estatal del Carchi"
    certificado.get_subject().OU = "UPEC"
    certificado.get_subject().CN = "UIAPP"
    certificado.get_subject().emailAddress = "info@upec.edu.ec"
    # Número de serie del certificado
    # Lo obtendremos de forma aleatoria, usando la hora actual y multiplicándola por 10
    # Este dato aparecerá en el campo "Número de serie" del certificado
    certificado.set_serial_number(int(time.time() * 10))
    # Inicio validez del certificado
    certificado.gmtime_adj_notBefore(0)  # En la fecha actual
    # Fecha de expiración del certificado, le asignaremos 10 años
    certificado.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    # Campo Asunto del certificado
    # Asignaremos el mismo valor que el Emisor ("Universidad")
    certificado.set_issuer(certificado.get_subject())
    certificado.set_pubkey(parDeClaves)
    certificado.sign(parDeClaves, 'md5')  # también podría ser cert.sign(pKey, 'sha256')
    return certificado

"""
Para crear un par de claves pública/privada
    Argumentos: tipo - Tipo de clave (TYPE_RSA o TYPE_DSA)
                bits - Números de bits para usar en la clave (1024, 2048 ó 4096)
    Devuelve: el par de claves pública/privada en un objeto PKey
"""
def CrearParDeClaves(tipo, bits):
    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(tipo, bits)
    return pkey

"""
Para generar el certificado autofirmado
"""
def GenerarCertificado():  
    if os.path.exists(f"{rutaCertificado}certificate.cer"):
        return  
    resumenAcciones = {}
    resumenAcciones['Versión OpenSSL'] = OpenSSL.__version__
    # Generando Clave Privada para el certificado...
    Clave = CrearParDeClaves(OpenSSL.crypto.TYPE_RSA, 1024)
    # Codificado PEM
    # Generará un fichero .pem con la clave privada
    # Este fichero nunca debe ser revelado
    with open(f'{rutaCertificado}private_key.pem', 'wb') as pk:
        pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, Clave)
        pk.write(pk_str)
        # Mostramos la clave privada sólo para depuración
        # En un programa en producción NUNCA debe mostrarse esta clave
        resumenAcciones['Clave Privada'] = pk_str    
    # Generando una certificación de cliente autofirmada ...
    certificado = CrearCertificadoAutofirmado(parDeClaves=Clave)
    with open(f'{rutaCertificado}certificate.cer', 'wb') as cer:
        cer_str = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, certificado)
        cer.write(cer_str)
        resumenAcciones['Certificado autofirmado'] = cer_str
    # Generando la clave pública ...
    with open(f'{rutaCertificado}public_key.pem', 'wb') as pub_key:
        pub_key_str = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, certificado.get_pubkey())
        pub_key.write(pub_key_str)
        resumenAcciones['Clave pública'] = pub_key_str
    # Take a private key and a certificate and combine them into a PKCS12 file.
    # Generating a container file of the private key and the certificate...
    # Usa la clave privada y el certificado y los combina en un archivo PKCS12
    # Generando un archivo contenedor de la clave privada y el certificado ...
    p12 = OpenSSL.crypto.PKCS12()
    p12.set_privatekey(Clave)
    p12.set_certificate(certificado)
    # El archivo PKSC12 (.pfx) puede convertirse a formato PEM
    open(f'{rutaCertificado}container.pfx', 'wb').write(p12.export())
    # Mostrar el resumen de acciones
    print("*******************")
    print("\n".join("{}:{}".format(i, j) for i, j in resumenAcciones.items()))
    print("*******************")
    return True