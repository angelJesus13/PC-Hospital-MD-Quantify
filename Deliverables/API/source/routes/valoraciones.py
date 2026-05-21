"""routes/valoraciones.py — Escalas clínicas SQL + detalle MongoDB"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models import MdValoraciones, MdPacientes
from schemas import ValoracionCreate, ValoracionResponse
from auth import require_any, require_medico
from mongo_database import get_valoraciones_collection, get_logs_collection
from utils.helpers import clasificar_glasgow
from datetime import datetime, timezone

router = APIRouter(prefix="/valoraciones", tags=["Valoraciones"])


def _auto_clasificar(escala: str, total: float | None, componentes: dict | None) -> str:
    """Determina el nivel de alerta según la escala y puntaje."""
    if escala == "Glasgow" and total is not None:
        if total >= 13:
            return "NORMAL"
        elif total >= 9:
            return "MODERADO"
        else:
            return "CRITICO"
    elif escala == "MEWS" and total is not None:
        if total <= 4:
            return "NORMAL"
        elif total <= 6:
            return "ALTO"
        else:
            return "CRITICO"
    elif escala == "APGAR" and total is not None:
        if total >= 7:
            return "NORMAL"
        elif total >= 4:
            return "MODERADO"
        else:
            return "CRITICO"
    return "NORMAL"


@router.post("/", response_model=ValoracionResponse, status_code=status.HTTP_201_CREATED)
async def create_valoracion(
    data: ValoracionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    if not db.query(MdPacientes).filter(MdPacientes.id == data.paciente_id).first():
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Calcular total si hay componentes numéricos
    total = None
    if data.componentes and data.escala == "Glasgow":
        comps = data.componentes
        total = sum([
            comps.get("apertura_ocular", {}).get("valor", 0),
            comps.get("respuesta_verbal", {}).get("valor", 0),
            comps.get("respuesta_motora", {}).get("valor", 0),
        ])

    nivel = _auto_clasificar(data.escala, total, data.componentes)

    # Registro SQL (resumen)
    val_sql = MdValoraciones(
        paciente_id=data.paciente_id,
        escala=data.escala,
        resultado=str(total) if total is not None else data.resultado,
        observaciones=data.observaciones,
        fecha=data.fecha,
        registrado_por=data.registrado_por or current_user.id,
    )
    db.add(val_sql)
    db.commit()
    db.refresh(val_sql)

    # Registro MongoDB (detalle completo)
    val_col = get_valoraciones_collection()
    now = datetime.now(timezone.utc)
    requiere_intervencion = nivel in ("CRITICO", "EMERGENCIA")

    interpretacion = ""
    if data.escala == "Glasgow" and total is not None:
        interpretacion = f"GCS = {total} — {clasificar_glasgow(int(total))}"
        if total <= 8:
            interpretacion += ". Requiere UCI."

    await val_col.insert_one({
        "paciente_id": data.paciente_id,
        "valoracion_sql_id": val_sql.id,
        "registrado_por_id": current_user.id,
        "tipo": data.escala,
        "nivel": nivel,
        "componentes": data.componentes,
        "total": float(total) if total is not None else None,
        "interpretacion": interpretacion or data.observaciones,
        "requiere_intervencion": requiere_intervencion,
        "notificado": requiere_intervencion,
        "accion_tomada": f"Protocolo {'UCI' if requiere_intervencion else 'estándar'} activado.",
        "timestamp": now,
    })

    # Log de auditoría
    logs = get_logs_collection()
    await logs.insert_one({
        "usuario_id": current_user.id, "username": current_user.username,
        "ip_address": "system", "accion": "CREATE_VALORACION",
        "entidad_afectada": {"tipo": "valoracion", "id": val_sql.id,
                              "tabla": "md_valoraciones"},
        "resultado": "EXITO", "codigo_http": 201,
        "nivel": "EMERGENCIA" if requiere_intervencion else "INFO",
        "timestamp": now,
    })

    return val_sql


@router.get("/", response_model=list[ValoracionResponse])
def list_valoraciones(
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    paciente_id: int = Query(None),
    escala: str = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
):
    query = db.query(MdValoraciones).order_by(MdValoraciones.fecha.desc())
    if paciente_id:
        query = query.filter(MdValoraciones.paciente_id == paciente_id)
    if escala:
        query = query.filter(MdValoraciones.escala == escala)
    offset = (pagina - 1) * limite
    return query.offset(offset).limit(limite).all()


@router.get("/{val_id}", response_model=ValoracionResponse)
def get_valoracion(
    val_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    val = db.query(MdValoraciones).filter(MdValoraciones.id == val_id).first()
    if not val:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    return val


@router.get("/{val_id}/detalle")
async def get_valoracion_detalle(
    val_id: int,
    current_user=Depends(require_any),
):
    """Retorna el detalle completo de la valoración desde MongoDB."""
    val_col = get_valoraciones_collection()
    doc = await val_col.find_one(
        {"valoracion_sql_id": val_id}, {"_id": 0}
    )
    if not doc:
        raise HTTPException(status_code=404,
                            detail="Detalle MongoDB no encontrado para esta valoración")
    return doc
