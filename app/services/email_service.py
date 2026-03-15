import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings


def send_reset_email(to_email: str, name: str, token: str):
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    subject = "Password Reset Request"
    body = f"""
    <h2>Hi {name},</h2>
    <p>You requested a password reset. Click the link below to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    <p>This link expires in 1 hour.</p>
    <p>If you didn't request this, ignore this email.</p>
    """
    _send_email(to_email, subject, body)


def _send_email(to: str, subject: str, html: str):
    if not settings.SMTP_USER:
        print(f"[EMAIL MOCK] To: {to} | Subject: {subject}")
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, to, msg.as_string())
