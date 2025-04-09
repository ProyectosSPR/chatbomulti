# backend/app/core/logger.py

import logging
import sys

# Crear un logger global para todo el proyecto
logger = logging.getLogger("chatbot_backend")
logger.setLevel(logging.INFO)

# Evitar duplicados
if not logger.hasHandlers():
    # Handler para consola (ideal para desarrollo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # Handler para archivo de log (opcional)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Registrar ambos
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
