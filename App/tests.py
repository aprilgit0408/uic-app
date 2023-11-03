from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
USER_MAIL = 'uicapp_upec@hotmail.com'
mensaje = MIMEMultipart()
mensaje['From'] = USER_MAIL
mensaje['To'] = 'josaerick@gmail.com'
mensaje['Subject'] = 'Prueba de email'

mailServer = SMTP('smtp.office365.com', port=587)
mailServer.starttls()
mailServer.login(USER_MAIL, 'Uicapp123')
mensaje.attach(MIMEText('Hola mundo', 'html'))
mailServer.sendmail(USER_MAIL, 'josaerick@gmail.com'.split(','), mensaje.as_string())
print('Mails enviados a: ', 'josaerick@gmail.com')
mailServer.quit()