import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings

async def send_reset_email(to_email: str, reset_token: str):
    try:
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_user = settings.EMAIL_USERNAME
        smtp_password = settings.EMAIL_PASSWORD

        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = "Redefinição de Senha"

        body = f"Clique no link para redefinir sua senha: http://localhost:3000/resetPassword?token={reset_token}"
        msg.attach(MIMEText(body, "plain"))

        # Conectar ao servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia TLS
        server.login(smtp_user, smtp_password)
        server.sendmail(settings.EMAIL_SENDER, to_email, msg.as_string())
        server.quit()

        print(f"E-mail enviado para {to_email}")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
