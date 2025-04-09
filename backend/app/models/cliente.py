# backend/app/models/cliente.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)

    # Relación con usuarios
    usuarios = relationship("Usuario", back_populates="cliente")
