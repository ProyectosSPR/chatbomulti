from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, field_validator
import re

class ResetPasswordRequest(BaseModel):
    token: str
    nueva_contrasena: str
    @field_validator("nueva_contrasena")
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
       