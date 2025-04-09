# backend/app/core/mail_config.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings
conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,   
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,     
    USE_CREDENTIALS = True
)


async def enviar_correo_recuperacion(destinatario: EmailStr, token: str):
    link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    mensaje = MessageSchema(
        subject="🔐 Recupera tu contraseña",
        recipients=[destinatario],
        body=f"Hola,\n\nPara restablecer tu contraseña, haz clic en este enlace:\n{link}\n\nEste enlace expira en 30 minutos.",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(mensaje)
