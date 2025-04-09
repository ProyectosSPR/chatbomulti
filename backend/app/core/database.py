# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crear motor de conexión a base de datos
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarador de modelos
Base = declarative_base()
