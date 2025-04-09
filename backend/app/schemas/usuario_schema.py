# app/schemas/usuario_schema.py
# ----------------------------------
# Esquemas (schemas) Pydantic para validar datos de entrada y salida
# relacionados con usuarios: registro, login y respuesta al cliente.
# ----------------------------------

from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, validator
import re

# Schema para recibir datos de registro
from pydantic import BaseModel, EmailStr, field_validator
import re

class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validar_fuerza_contrasena(cls, value):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Debe contener al menos una mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("Debe contener al menos una minúscula")
        if not re.search(r"\d", value):
            raise ValueError("Debe contener al menos un número")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Debe contener al menos un carácter especial")
        return value

# Schema para datos del login
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Schema de respuesta al cliente al registrar o autenticar un usuario
class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str


class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "usuario"  # ✅ por defecto se asigna "usuario"

    @field_validator("password")
    @classmethod
    def validar_fuerza_contrasena(cls, value):
        # validaciones de seguridad...
        return value


class UsuarioListado(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str

    class Config:
        orm_mode = True
