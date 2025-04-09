from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from datetime import datetime, timezone
from app.core.database import Base

class TokenRecuperacion(Base):
    __tablename__ = "tokens_recuperacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expiracion = Column(DateTime, nullable=False)
    usado = Column(Boolean, default=False)

    usuario = relationship("Usuario", backref="tokens_recuperacion")

    @staticmethod
    def generar_expiracion(minutos=30):
        return datetime.now(timezone.utc) + timedelta(minutes=minutos)
