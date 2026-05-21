"""routes/signos_vitales.py — Registro de signos vitales y alertas MEWS"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models import MdSignosVitales, MdPacientes
from schemas import SignosVitalesCreate, SignosVitalesResponse
from auth import require_any, get_current_user
from mongo_database import get_logs_collection, get_valoraciones_collection
from utils.helpers import calcular_mews
from datetime import datetime, timezone

router = APIRouter(prefix="/signos-vitales", tags=["Signos Vitales"])


@router.post("/", response_model=SignosVitalesResponse, status_code=status.HTTP_201_CREATED)
async def create_signos(
    data: SignosVitalesCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    if not db.query(MdPacientes).filter(MdPacientes.id == data.paciente_id).first():
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Calcular score MEWS automáticamente
    score_mews, nivel_mews = calcular_mews(
        frecuencia_cardiaca=data.frecuencia_cardiaca,
        frecuencia_respiratoria=data.frecuencia_respiratoria,
        saturacion_o2=data.saturacion_o2,
        temperatura=float(data.temperatura) if data.temperatura else None,
        escala_consciencia=data.escala_consciencia,
    )

    # Crear registro SQL
    signos_data = data.model_dump()
    signos_data["score_mews"] = score_mews
    signos = MdSignosVitales(**signos_data)
    db.add(signos)
    db.commit()
    db.refresh(signos)

    val_col = get_valoraciones_collection()
    logs = get_logs_collection()
    now = datetime.now(timezone.utc)

    # Log de auditoría
    await logs.insert_one({
        "usuario_id": current_user.id, "username": current_user.username,
        "ip_address": "system", "accion": "CREATE_SIGNOS",
        "entidad_afectada": {"tipo": "signos_vitales", "id": signos.id,
                              "tabla": "md_signos_vitales"},
        "resultado": "EXITO", "codigo_http": 201, "nivel": "INFO",
        "timestamp": now,
    })

    # Alerta automática si MEWS >= 5 (CRITICO)
    if score_mews >= 5:
        # Detectar parámetros violados
        parametros_violados = []
        if data.frecuencia_cardiaca and (data.frecuencia_cardiaca < 40 or data.frecuencia_cardiaca > 130):
            parametros_violados.append({"campo": "frecuencia_cardiaca",
                                         "valor_real": data.frecuencia_cardiaca,
                                         "umbral": "< 40 o > 130 lpm"})
        if data.saturacion_o2 and data.saturacion_o2 < 90:
            parametros_violados.append({"campo": "saturacion_o2",
                                         "valor_real": data.saturacion_o2,
                                         "umbral": "< 90%"})
        if data.frecuencia_respiratoria and data.frecuencia_respiratoria > 30:
            parametros_violados.append({"campo": "frecuencia_respiratoria",
                                         "valor_real": data.frecuencia_respiratoria,
                                         "umbral": "> 30 rpm"})

        tipo_alerta = "CODIGO_AZUL" if score_mews >= 7 else "MEWS_CRITICO"
        nivel_alerta = "EMERGENCIA" if score_mews >= 7 else "CRITICO"

        await val_col.insert_one({
            "paciente_id": data.paciente_id,
            "tipo": "alerta_vital",
            "nivel": nivel_alerta,
            "componentes": {
                "parametros_violados": parametros_violados,
                "score_mews": score_mews,
                "tipo_alerta": tipo_alerta,
            },
            "total": float(score_mews),
            "interpretacion": f"MEWS={score_mews}. {tipo_alerta} activado.",
            "requiere_intervencion": True,
            "notificado": True,
            "timestamp": now,
        })

        await logs.insert_one({
            "usuario_id": current_user.id, "username": current_user.username,
            "ip_address": "system", "accion": "ALERT_TRIGGERED",
            "entidad_afectada": {"tipo": "paciente", "id": data.paciente_id,
                                  "tabla": "md_signos_vitales"},
            "resultado": "EXITO", "codigo_http": 200,
            "nivel": "EMERGENCIA" if score_mews >= 7 else "ADVERTENCIA",
            "timestamp": now,
        })

    return signos


@router.get("/", response_model=list[SignosVitalesResponse])
def list_signos(
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    paciente_id: int = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
):
    query = db.query(MdSignosVitales).order_by(MdSignosVitales.fecha.desc())
    if paciente_id:
        query = query.filter(MdSignosVitales.paciente_id == paciente_id)
    offset = (pagina - 1) * limite
    return query.offset(offset).limit(limite).all()


@router.get("/{sv_id}", response_model=SignosVitalesResponse)
def get_signos(
    sv_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    sv = db.query(MdSignosVitales).filter(MdSignosVitales.id == sv_id).first()
    if not sv:
        raise HTTPException(status_code=404, detail="Registro de signos vitales no encontrado")
    return sv
