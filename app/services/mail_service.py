import aiosmtplib
from email.message import EmailMessage
from app.core import settings
class MailServices:
    async def send_email(self, to:str, subject:str, body:str) -> None:
        message = EmailMessage()
        message["From"] = settings.MAIL_USERNAME
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.EMAIL_SMTP_SERVER,
            port=settings.EMAIL_SMTP_PORT,
            username=settings.MAIL_USERNAME,
            password=settings.MAIL_PASSWORD,
            use_tls=True
        )