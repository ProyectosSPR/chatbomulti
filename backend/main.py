# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.models import usuario, cliente,token, refresh_token # 👈 asegura que se registren las tablas
from app.core.database import engine, Base
from app.core.logger import logger
from app.routes.auth_routes import router as auth_router
# ✅ Importación del router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando backend y creando base de datos...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("🛑 Deteniendo backend...")

app = FastAPI(title="Chatbot Multicliente", lifespan=lifespan)

# Habilitar CORS (para conectar con frontend como Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplazar con dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Registrar el router de autenticación
app.include_router(auth_router)

# Ruta raíz para prueba
@app.get("/")
def root():
    logger.info("📡 Solicitud a ruta raíz /")
    return {"message": "🚀 Backend funcionando correctamente"}
