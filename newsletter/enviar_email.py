import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_email(destinatario, assunto, corpo, anexo_path):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  

    email_origem = '' # email do codettes
    senha = '' # senha do email do codettes

    msg = MIMEMultipart()
    msg['From'] = email_origem
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    with open(anexo_path, 'rb') as arquivo:
        anexo = MIMEBase('application', 'octet-stream')
        anexo.set_payload(arquivo.read())
    
    encoders.encode_base64(anexo)
    
    anexo.add_header('Content-Disposition', f'attachment; filename= {anexo_path}')
    
    msg.attach(anexo)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia a conexão TLS
        server.login(email_origem, senha)
        server.sendmail(email_origem, destinatario, msg.as_string())
        server.quit()
        print('Email enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar email: {str(e)}')

destinatario = [] # emails para enviar
assunto = 'Codettes'
anexo_path = 'test.md'

def read_md_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

corpo = read_md_to_string(anexo_path)

for email in destinatario:
    enviar_email(email, assunto, corpo, anexo_path)
