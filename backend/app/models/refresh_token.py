from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.core.database import Base
from datetime import datetime, timezone

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    token = Column(String, unique=True, nullable=False)
    expiracion = Column(DateTime, nullable=False)

    usuario = relationship("Usuario", backref="refresh_tokens")

    @staticmethod
    def generar_expiracion(dias=7):
        return datetime.now(timezone.utc) + timedelta(days=dias)
