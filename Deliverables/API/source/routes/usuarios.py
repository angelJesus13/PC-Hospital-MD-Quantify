"""routes/usuarios.py — CRUD de usuarios y autenticación"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models import MdUsuarios
from schemas import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse,
    LoginRequest, TokenResponse,
)
from auth import (
    hash_password, authenticate_user, create_access_token,
    get_current_user, require_admin, require_any,
)
from mongo_database import get_logs_collection, get_telemetria_collection
from utils.helpers import get_turno_actual
from datetime import datetime, timezone
import uuid

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ── POST /auth/login ──────────────────────────────────────────────────────────
auth_router = APIRouter(prefix="/auth", tags=["Autenticación"])

@auth_router.post("/login", response_model=TokenResponse)
async def login(request: Request, form: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, form.username, form.password)
    ip = request.client.host if request.client else "unknown"

    logs = get_logs_collection()
    telemetria = get_telemetria_collection()

    if not user:
        await logs.insert_one({
            "usuario_id": None, "username": form.username,
            "ip_address": ip, "accion": "LOGIN_FAILED",
            "resultado": "FALLIDO", "codigo_http": 401,
            "nivel": "ADVERTENCIA", "timestamp": datetime.now(timezone.utc),
        })
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales inválidas")

    token, jti = create_access_token(user.id, user.username, user.role)
    expires_in = 480 * 60  # segundos

    # Log de auditoría
    await logs.insert_one({
        "usuario_id": user.id, "username": user.username,
        "ip_address": ip, "accion": "LOGIN", "resultado": "EXITO",
        "codigo_http": 200, "nivel": "INFO",
        "timestamp": datetime.now(timezone.utc),
    })
    # Telemetría de sesión
    await telemetria.insert_one({
        "token_jti": jti, "usuario_id": user.id, "username": user.username,
        "rol": user.role, "inicio_sesion": datetime.now(timezone.utc),
        "ip_address": ip, "turno": get_turno_actual(),
        "estado": "activa", "requests_totales": 0,
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc),
    })

    return TokenResponse(
        access_token=token,
        expires_in=expires_in,
        usuario_id=user.id,
        username=user.username,
        role=user.role,
    )


@auth_router.post("/logout")
async def logout(current_user: MdUsuarios = Depends(get_current_user)):
    telemetria = get_telemetria_collection()
    now = datetime.now(timezone.utc)
    await telemetria.update_one(
        {"usuario_id": current_user.id, "estado": "activa"},
        {"$set": {"estado": "cerrada", "fin_sesion": now,
                  "cerrado_por": "usuario", "updatedAt": now}},
        sort=[("inicio_sesion", -1)]
    )
    return {"message": "Sesión cerrada correctamente"}


# ── CRUD Usuarios (solo admin) ────────────────────────────────────────────────

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: MdUsuarios = Depends(require_admin),
):
    if db.query(MdUsuarios).filter(
        (MdUsuarios.username == data.username) | (MdUsuarios.email == data.email)
    ).first():
        raise HTTPException(status_code=409,
                            detail="Username o email ya registrado")
    user = MdUsuarios(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=list[UsuarioResponse])
def list_usuarios(
    db: Session = Depends(get_db),
    current_user: MdUsuarios = Depends(require_admin),
    pagina: int = 1,
    limite: int = 20,
):
    offset = (pagina - 1) * limite
    return db.query(MdUsuarios).offset(offset).limit(limite).all()


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: MdUsuarios = Depends(require_any)):
    return current_user


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: MdUsuarios = Depends(require_admin),
):
    user = db.query(MdUsuarios).filter(MdUsuarios.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: MdUsuarios = Depends(require_admin),
):
    user = db.query(MdUsuarios).filter(MdUsuarios.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: MdUsuarios = Depends(require_admin),
):
    user = db.query(MdUsuarios).filter(MdUsuarios.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.activo = False  # Soft delete
    db.commit()
