import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_reset_email(to_email: str, token: str):
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Redefinição de senha"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Redefinição de Senha</h2>
        <p>Recebemos uma solicitação para redefinir sua senha.</p>
        <p>Clique no botão abaixo para criar uma nova senha. O link é válido por <strong>1 hora</strong>.</p>
        <a href="{reset_link}"
           style="display:inline-block;padding:12px 24px;background:#4F46E5;color:#fff;
                  text-decoration:none;border-radius:6px;font-weight:bold;">
          Redefinir Senha
        </a>
        <p style="margin-top:20px;color:#888;font-size:12px;">
          Se você não solicitou isso, ignore este email.
        </p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
    except Exception as e:
        print(f"[Email Error] {e}")
