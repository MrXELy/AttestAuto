from getpass import getpass

try:
    from password import pw
    password = pw
except ModuleNotFoundError:
    password = getpass()
    
SENDER_EMAIL = "your@mail"

import smtplib, ssl, email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver_email, dir_path, filename):
    """Send an email with a file attached

    :param receiver_email: Email adress to send to
    :type receiver_email: str
    :param dir_path: Directory path of the file to attach
    :type dir_path: str
    :param filename: File name
    :type filename: str
    """
    print('[LOG] Sending email...')
    smtp_server = "smtp.gmail.com"
    port = 587
    subject = "Attestation"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject

    # Open PDF file in binary mode
    with open(dir_path + filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SENDER_EMAIL, password)
        server.sendmail(SENDER_EMAIL, receiver_email, text)
        print(f'[SUCCESS] Email sent to {receiver_email}')
    except Exception as e:
        print('[FAIL]', e)
    finally:
        server.quit()