# app/auth/auth_routes.py
# ----------------------------------
# Endpoints para registrar nuevos usuarios y autenticarlos (login).
# Utiliza seguridad con JWT y hash de contraseñas.
# ----------------------------------

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioRegistro, UsuarioLogin, UsuarioRespuesta
from app.models.usuario import Usuario
from app.core.database import SessionLocal
from app.auth.security import hashear_password, verificar_password, crear_token_acceso , get_current_user ,require_role
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioRespuesta
from uuid import uuid4
from datetime import datetime
from app.schemas.forgot_password import ForgotPasswordRequest
from app.models.token import TokenRecuperacion
from app.core.mail_config import enviar_correo_recuperacion
from app.schemas.reset_password import ResetPasswordRequest
from app.models.refresh_token import RefreshToken
from app.schemas.token import TokenEntrada
from datetime import datetime, timezone
from app.schemas.usuario_schema import UsuarioListado

# Creamos el router para agrupar rutas relacionadas con autenticación
router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Dependencia reutilizable para abrir y cerrar sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registro de usuario
@router.post("/register", response_model=UsuarioRespuesta)
def registrar(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    # Validar si ya existe un usuario con ese email
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear nuevo usuario con contraseña hasheada
    nuevo = Usuario(
            nombre=usuario.nombre,
        email=usuario.email,
        password_hash=hashear_password(usuario.password),
        rol=usuario.rol
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo  # Se devuelve en formato limpio (sin contraseña)

# Login: valida email y contraseña y devuelve un JWT
@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if not db_user or not verificar_password(usuario.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = crear_token_acceso({"sub": str(db_user.id)})

    # Limitar a 3 tokens máximo por usuario
    tokens_activos = db.query(RefreshToken).filter(
        RefreshToken.usuario_id == db_user.id
    ).order_by(RefreshToken.expiracion.asc()).all()

    if len(tokens_activos) >= 3:
        # Elimina el más antiguo
        db.delete(tokens_activos[0])
        db.commit()

    # Crear nuevo refresh token
    refresh_token_str = str(uuid4())
    nuevo_token = RefreshToken(
        usuario_id=db_user.id,
        token=refresh_token_str,
        expiracion=RefreshToken.generar_expiracion()
    )

    db.add(nuevo_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }

# ✅ Ruta protegida para obtener el usuario actual a partir del token
@router.get("/me", response_model=UsuarioRespuesta)
def obtener_usuario_actual(usuario: Usuario = Depends(get_current_user)):
    return usuario



@router.post("/forgot-password")
async def solicitar_recuperacion(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="El email no está registrado")

    # Generar token único
    token_str = str(uuid4())
    expiracion = TokenRecuperacion.generar_expiracion()

    # Guardar token en la base de datos
    token = TokenRecuperacion(
        usuario_id=usuario.id,
        token=token_str,
        expiracion=expiracion,
    )
    db.add(token)
    db.commit()

    # Enviar correo con el token
    await enviar_correo_recuperacion(request.email, token_str)

    return {"message": "Se ha enviado un correo con instrucciones para restablecer tu contraseña."}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_obj = db.query(TokenRecuperacion).filter(TokenRecuperacion.token == request.token).first()

    if not token_obj:
        raise HTTPException(status_code=404, detail="Token no válido")

    if token_obj.usado:
        raise HTTPException(status_code=400, detail="Este token ya fue usado")

    if token_obj.expiracion < datetime.utcnow():
        raise HTTPException(status_code=400, detail="El token ha expirado")

    usuario = db.query(Usuario).filter(Usuario.id == token_obj.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.password_hash = hashear_password(request.nueva_contrasena)
    token_obj.usado = True  # Marcar token como usado

    db.commit()

    return {"message": "Contraseña actualizada correctamente"}

@router.post("/refresh")
def refresh_token(payload: TokenEntrada, db: Session = Depends(get_db)):
    token_str = payload.token

    token_obj = db.query(RefreshToken).filter(RefreshToken.token == token_str).first()

    if not token_obj:
        raise HTTPException(status_code=401, detail="Token no válido")

    if token_obj.expiracion < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token expirado")

    new_access_token = crear_token_acceso({"sub": str(token_obj.usuario_id)})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



@router.post("/logout")
def logout(payload: TokenEntrada, db: Session = Depends(get_db)):
    token_str = payload.token

    token_obj = db.query(RefreshToken).filter(RefreshToken.token == token_str).first()
    if not token_obj:
        raise HTTPException(status_code=404, detail="Token no encontrado")

    db.delete(token_obj)
    db.commit()

    return {"message": "Sesión cerrada correctamente"}
@router.post("/logout-all")
def logout_de_todas_las_sesiones(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tokens = db.query(RefreshToken).filter(RefreshToken.usuario_id == usuario.id).all()

    for token in tokens:
        db.delete(token)

    db.commit()

    return {"message": "Todas las sesiones han sido cerradas"}



router.get("/solo-admin")
def ruta_admin(usuario: Usuario = Depends(require_role("admin"))):
    return {"message": f"Hola {usuario.nombre}, eres administrador."}


@router.get("/solo-agente")
def ruta_agente(usuario: Usuario = Depends(require_role("agente"))):
    return {"message": f"Hola {usuario.nombre}, eres agente autorizado."}


 # si usas un schema, opcional

@router.put("/cambiar-rol/{usuario_id}")
def cambiar_rol_de_usuario(
    usuario_id: int,
    nuevo_rol: str,
    admin: Usuario = Depends(require_role("admin")),  # solo admins pueden cambiar roles
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.rol = nuevo_rol
    db.commit()
    return {"message": f"Rol actualizado a '{nuevo_rol}' para {usuario.email}"}


@router.get("/usuarios", response_model=list[UsuarioListado])
def listar_usuarios(admin: Usuario = Depends(require_role("admin")), db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios