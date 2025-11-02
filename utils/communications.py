import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Se define una función para enviar correos:
def send_email(destiny_email, title, message):
    email = "task.m4nager@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = destiny_email
    msg['Subject'] = title
    msg.attach(MIMEText(message, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(email, os.getenv('EMAIL_PASS'))
        servidor.sendmail(email, destiny_email, msg.as_string())
        servidor.quit()
        return(True)
    except:
        return(False)