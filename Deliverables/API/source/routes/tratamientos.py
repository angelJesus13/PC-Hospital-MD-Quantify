"""routes/tratamientos.py — Prescripciones con detección de interacciones farmacológicas"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models import MdTratamientos, MdDiagnostico, MdNotasMedicas
from schemas import TratamientoCreate, TratamientoResponse
from auth import require_any, require_medico
from mongo_database import get_logs_collection, get_valoraciones_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])

# Tabla básica de interacciones farmacológicas (en producción: usar base de datos)
INTERACCIONES_CONOCIDAS = {
    ("enalapril", "ibuprofeno"): {
        "severidad": "Mayor",
        "mecanismo": "Los AINEs reducen el efecto antihipertensivo de los IECA y pueden deteriorar la función renal",
        "referencia": "Micromedex 2.0",
    },
    ("warfarina", "aspirina"): {
        "severidad": "Mayor",
        "mecanismo": "Riesgo aumentado de sangrado por inhibición plaquetaria aditiva",
        "referencia": "Micromedex 2.0",
    },
    ("metformina", "contraste_yodado"): {
        "severidad": "Mayor",
        "mecanismo": "Riesgo de acidosis láctica por acumulación de metformina",
        "referencia": "Micromedex 2.0",
    },
}


def _check_interaccion(med_nuevo: str, meds_activos: list[str]) -> dict | None:
    """Verifica si el nuevo medicamento tiene interacción con algún activo."""
    nuevo = med_nuevo.lower().split()[0]
    for activo in meds_activos:
        activo_nombre = activo.lower().split()[0]
        clave1 = (nuevo, activo_nombre)
        clave2 = (activo_nombre, nuevo)
        if clave1 in INTERACCIONES_CONOCIDAS:
            return {"medicamento_activo": activo, **INTERACCIONES_CONOCIDAS[clave1]}
        if clave2 in INTERACCIONES_CONOCIDAS:
            return {"medicamento_activo": activo, **INTERACCIONES_CONOCIDAS[clave2]}
    return None


@router.post("/", response_model=TratamientoResponse, status_code=status.HTTP_201_CREATED)
async def create_tratamiento(
    data: TratamientoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    dx = db.query(MdDiagnostico).filter(MdDiagnostico.id == data.diagnostico_id).first()
    if not dx:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")

    # Obtener medicamentos activos del mismo paciente
    nota = db.query(MdNotasMedicas).filter(MdNotasMedicas.id == dx.nota_id).first()
    if nota:
        meds_activos_qs = (
            db.query(MdTratamientos.medicamento)
            .join(MdDiagnostico, MdTratamientos.diagnostico_id == MdDiagnostico.id)
            .join(MdNotasMedicas, MdDiagnostico.nota_id == MdNotasMedicas.id)
            .filter(
                MdNotasMedicas.paciente_id == nota.paciente_id,
                MdTratamientos.activo == True,
            )
            .all()
        )
        meds_activos = [m[0] for m in meds_activos_qs]

        # Chequeo de interacciones
        interaccion = _check_interaccion(data.medicamento, meds_activos)
        if interaccion and not data.forzar_prescripcion:
            val_col = get_valoraciones_collection()
            await val_col.insert_one({
                "paciente_id": nota.paciente_id,
                "tipo": "interaccion_farmacologica",
                "nivel": "ALTO",
                "componentes": {
                    "medicamento_activo": interaccion["medicamento_activo"],
                    "medicamento_nuevo": data.medicamento,
                    "mecanismo": interaccion["mecanismo"],
                    "referencia": interaccion["referencia"],
                    "severidad_interaccion": interaccion["severidad"],
                },
                "interpretacion": f"Interacción {interaccion['severidad']} detectada.",
                "requiere_intervencion": False,
                "notificado": True,
                "timestamp": datetime.now(timezone.utc),
            })
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "advertencia": (
                        f"Interacción potencial: {interaccion['mecanismo']}. "
                        f"Referencia: {interaccion['referencia']}. "
                        "Para forzar prescripción, enviar 'forzar_prescripcion: true'."
                    )
                },
            )

    # Crear tratamiento
    tx_data = data.model_dump(exclude={"forzar_prescripcion"})
    tx = MdTratamientos(**tx_data)
    db.add(tx)
    db.commit()
    db.refresh(tx)

    logs = get_logs_collection()
    await logs.insert_one({
        "usuario_id": current_user.id, "username": current_user.username,
        "ip_address": "system", "accion": "CREATE_TRATAMIENTO",
        "entidad_afectada": {"tipo": "tratamiento", "id": tx.id,
                              "tabla": "md_tratamientos"},
        "resultado": "EXITO", "codigo_http": 201, "nivel": "INFO",
        "timestamp": datetime.now(timezone.utc),
    })
    return tx


@router.get("/", response_model=list[TratamientoResponse])
def list_tratamientos(
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    diagnostico_id: int = Query(None),
    activo: bool = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
):
    query = db.query(MdTratamientos)
    if diagnostico_id:
        query = query.filter(MdTratamientos.diagnostico_id == diagnostico_id)
    if activo is not None:
        query = query.filter(MdTratamientos.activo == activo)
    offset = (pagina - 1) * limite
    return query.offset(offset).limit(limite).all()


@router.get("/{tx_id}", response_model=TratamientoResponse)
def get_tratamiento(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    tx = db.query(MdTratamientos).filter(MdTratamientos.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    return tx


@router.patch("/{tx_id}/suspender")
def suspender_tratamiento(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    tx = db.query(MdTratamientos).filter(MdTratamientos.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Tratamiento no encontrado")
    tx.activo = False
    db.commit()
    return {"message": f"Tratamiento {tx_id} suspendido"}
