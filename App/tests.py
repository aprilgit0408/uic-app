from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
USER_MAIL = 'uicappupec@outlook.com'
print('inicio menjsaes')
try:
    mensaje = MIMEMultipart()
    mensaje['From'] = USER_MAIL
    mensaje['To'] = 'josaerick@gmail.com'
    mensaje['Subject'] = 'asunto'

    mailServer = SMTP('smtp-mail.outlook.com',587)
    mailServer.starttls()
    mailServer.login(USER_MAIL, 'Admin12-upec')
    mailServer.sendmail(USER_MAIL, 'josaerick@gmail.com', mensaje.as_string())
    print('Mails enviados a: ', 'josaerick@gmail.com')
    mailServer.quit()
except Exception as e:
    print('error: ', e)