"""
auth.py — Autenticación JWT y control de roles
Incluye: creación de tokens, validación, hash de contraseñas, guards de rol
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import MdUsuarios
from schemas import TokenData, RolSchema
from config import get_settings
import uuid

settings = get_settings()

# ── Contexto de hashing ───────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# ── Bearer token extractor ────────────────────────────────────────────────────
bearer_scheme = HTTPBearer()


# ── Funciones de contraseña ───────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Genera hash bcrypt con factor de costo 12."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica contraseña contra hash bcrypt almacenado."""
    return pwd_context.verify(plain_password, hashed_password)


# ── Funciones JWT ─────────────────────────────────────────────────────────────

def create_access_token(
    usuario_id: int,
    username: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, str]:
    """
    Crea un JWT de acceso.
    Retorna (token_string, jti) — jti para telemetría MongoDB.
    """
    jti = str(uuid.uuid4())  # JWT ID único para tracing/blacklist
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {
        "sub": str(usuario_id),
        "username": username,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": jti,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token, jti


def decode_token(token: str) -> TokenData:
    """
    Decodifica y valida un JWT.
    Lanza HTTPException 401 si el token es inválido o expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        usuario_id: int = int(payload.get("sub"))
        username: str = payload.get("username")
        role: str = payload.get("role")
        if usuario_id is None or username is None:
            raise credentials_exception
        return TokenData(
            usuario_id=usuario_id,
            username=username,
            role=RolSchema(role),
        )
    except JWTError:
        raise credentials_exception


# ── Dependencias FastAPI ──────────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> MdUsuarios:
    """
    Dependencia: extrae y valida el token JWT, retorna el usuario activo.
    """
    token_data = decode_token(credentials.credentials)
    user = db.query(MdUsuarios).filter(
        MdUsuarios.id == token_data.usuario_id,
        MdUsuarios.activo == True,
    ).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o desactivado",
        )
    return user


def require_role(*roles: RolSchema):
    """
    Factory de dependencias para guards de rol.
    Uso: Depends(require_role(RolSchema.admin))
    """
    def _role_guard(current_user: MdUsuarios = Depends(get_current_user)):
        if current_user.role not in [r.value for r in roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere rol: {[r.value for r in roles]}",
            )
        return current_user
    return _role_guard


# ── Shortcuts de roles ────────────────────────────────────────────────────────
require_admin = require_role(RolSchema.admin)
require_medico = require_role(RolSchema.admin, RolSchema.medico)
require_any = require_role(RolSchema.admin, RolSchema.medico, RolSchema.enfermero)


# ── Autenticación de usuario ──────────────────────────────────────────────────

def authenticate_user(db: Session, username: str, password: str) -> Optional[MdUsuarios]:
    """
    Autentica usuario por username y contraseña.
    Retorna el usuario ORM o None si las credenciales son inválidas.
    """
    user = db.query(MdUsuarios).filter(
        MdUsuarios.username == username,
        MdUsuarios.activo == True,
    ).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
