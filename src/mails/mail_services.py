import aiosmtplib
from email.message import EmailMessage
from src.setting import settings

class MailServices:
    async def send_email(self, to:str, subject:str, body:str) -> None:
        message = EmailMessage()
        message["From"] = settings.EMAIL_SMTP_USER
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.EMAIL_SMTP_SERVER,
            port=settings.EMAIL_SMTP_PORT,
            username=settings.EMAIL_SMTP_USER,
            password=settings.EMAIL_SMTP_PASSWORD,
            start_tls=True
        )