import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMPANY_EMAIL_ADDRESS = 'alivedead068@gmail.com'
PASSWORD = 'deadoraliveisasecret'

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def email_service(to_address, subject, message):
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(COMPANY_EMAIL_ADDRESS, PASSWORD)

    # setup the parameters of the message
    msg['From'] = COMPANY_EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject       
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg
    s.quit()

template_file = 'verify_mail_template.txt'
message_template = read_template(template_file)      
message = message_template.substitute(CUSTOMER_NAME=customer_name, CONFIRMATION_EMAIL=confirmation_url)
subject = 'DeadOrAlive: Confirm your email'
email_service(to_address, subject, message)
