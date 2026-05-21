"""routes/diagnostico.py — CRUD de diagnósticos con validación CIE-10"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models import MdDiagnostico, MdNotasMedicas
from schemas import DiagnosticoCreate, DiagnosticoResponse
from auth import require_any, require_medico
from mongo_database import get_logs_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/diagnostico", tags=["Diagnóstico"])


@router.post("/", response_model=DiagnosticoResponse, status_code=status.HTTP_201_CREATED)
async def create_diagnostico(
    data: DiagnosticoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    if not db.query(MdNotasMedicas).filter(MdNotasMedicas.id == data.nota_id).first():
        raise HTTPException(status_code=404, detail="Nota médica no encontrada")

    dx = MdDiagnostico(**data.model_dump())
    db.add(dx)
    db.commit()
    db.refresh(dx)

    logs = get_logs_collection()
    await logs.insert_one({
        "usuario_id": current_user.id, "username": current_user.username,
        "ip_address": "system", "accion": "CREATE_DIAGNOSTICO",
        "entidad_afectada": {"tipo": "diagnostico", "id": dx.id,
                              "tabla": "md_diagnostico"},
        "cambios": {"antes": None, "despues": {
            "nota_id": data.nota_id,
            "codigo_cie": data.codigo_cie,
            "severidad": data.severidad.value,
        }},
        "resultado": "EXITO", "codigo_http": 201, "nivel": "INFO",
        "timestamp": datetime.now(timezone.utc),
    })
    return dx


@router.get("/", response_model=list[DiagnosticoResponse])
def list_diagnosticos(
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    nota_id: int = Query(None),
    activo: bool = Query(None),
    codigo_cie: str = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
):
    query = db.query(MdDiagnostico)
    if nota_id:
        query = query.filter(MdDiagnostico.nota_id == nota_id)
    if activo is not None:
        query = query.filter(MdDiagnostico.activo == activo)
    if codigo_cie:
        query = query.filter(MdDiagnostico.codigo_cie == codigo_cie.upper())
    offset = (pagina - 1) * limite
    return query.offset(offset).limit(limite).all()


@router.get("/{dx_id}", response_model=DiagnosticoResponse)
def get_diagnostico(
    dx_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    dx = db.query(MdDiagnostico).filter(MdDiagnostico.id == dx_id).first()
    if not dx:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    return dx


@router.patch("/{dx_id}/desactivar", response_model=DiagnosticoResponse)
def desactivar_diagnostico(
    dx_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    dx = db.query(MdDiagnostico).filter(MdDiagnostico.id == dx_id).first()
    if not dx:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    dx.activo = False
    db.commit()
    db.refresh(dx)
    return dx
