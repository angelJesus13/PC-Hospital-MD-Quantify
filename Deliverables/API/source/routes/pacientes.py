"""routes/pacientes.py — CRUD de pacientes y expediente clínico"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import MdPacientes, MdNotasMedicas, MdDiagnostico, MdTratamientos, MdSignosVitales, MdValoraciones
from schemas import PacienteCreate, PacienteUpdate, PacienteResponse, ExpedienteResponse
from auth import get_current_user, require_any, require_admin, require_medico
from mongo_database import get_logs_collection, get_valoraciones_collection
from utils.helpers import paginar, calcular_paginas
from datetime import datetime, timezone

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
async def create_paciente(
    data: PacienteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    if db.query(MdPacientes).filter(MdPacientes.curp == data.curp).first():
        raise HTTPException(status_code=409,
                            detail=f"Ya existe un paciente con CURP: {data.curp}")
    paciente = MdPacientes(**data.model_dump())
    db.add(paciente)
    db.commit()
    db.refresh(paciente)

    # Log de auditoría MongoDB
    logs = get_logs_collection()
    await logs.insert_one({
        "usuario_id": current_user.id, "username": current_user.username,
        "ip_address": "system", "accion": "CREATE_PACIENTE",
        "entidad_afectada": {"tipo": "paciente", "id": paciente.id,
                              "tabla": "md_pacientes"},
        "cambios": {"antes": None, "despues": {"curp": data.curp,
                                                "nombre": data.nombre}},
        "resultado": "EXITO", "codigo_http": 201, "nivel": "INFO",
        "timestamp": datetime.now(timezone.utc),
    })
    return paciente


@router.get("/", response_model=dict)
def list_pacientes(
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
    nombre: str = Query(None),
    curp: str = Query(None),
):
    query = db.query(MdPacientes)
    if nombre:
        query = query.filter(MdPacientes.nombre.ilike(f"%{nombre}%"))
    if curp:
        query = query.filter(MdPacientes.curp == curp.upper())

    items, total = paginar(query, pagina, limite)
    return {
        "items": [PacienteResponse.model_validate(p) for p in items],
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "paginas_totales": calcular_paginas(total, limite),
    }


@router.get("/{paciente_id}", response_model=PacienteResponse)
def get_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    paciente = db.query(MdPacientes).filter(
        MdPacientes.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@router.put("/{paciente_id}", response_model=PacienteResponse)
async def update_paciente(
    paciente_id: int,
    data: PacienteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    paciente = db.query(MdPacientes).filter(
        MdPacientes.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(paciente, field, value)
    db.commit()
    db.refresh(paciente)
    return paciente


@router.get("/{paciente_id}/expediente")
async def get_expediente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=50),
):
    """Retorna el expediente clínico completo de un paciente (SQL + NoSQL)."""
    paciente = db.query(MdPacientes).filter(
        MdPacientes.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Notas médicas con joinedload para optimizar queries
    notas = (
        db.query(MdNotasMedicas)
        .options(joinedload(MdNotasMedicas.diagnosticos))
        .filter(MdNotasMedicas.paciente_id == paciente_id)
        .order_by(MdNotasMedicas.fecha.desc())
        .all()
    )

    signos = (
        db.query(MdSignosVitales)
        .filter(MdSignosVitales.paciente_id == paciente_id)
        .order_by(MdSignosVitales.fecha.desc())
        .limit(10)
        .all()
    )

    valoraciones = (
        db.query(MdValoraciones)
        .filter(MdValoraciones.paciente_id == paciente_id)
        .order_by(MdValoraciones.fecha.desc())
        .all()
    )

    # Alertas activas desde MongoDB
    val_col = get_valoraciones_collection()
    alertas_cursor = val_col.find(
        {"paciente_id": paciente_id, "requiere_intervencion": True},
        {"_id": 0}
    ).sort("timestamp", -1).limit(5)
    alertas = await alertas_cursor.to_list(length=5)

    return {
        "paciente": PacienteResponse.model_validate(paciente),
        "notas_medicas": [
            {"id": n.id, "tipo": n.tipo_nota, "fecha": n.fecha,
             "medico_id": n.medico_id,
             "diagnosticos": [{"id": d.id, "descripcion": d.descripcion,
                               "codigo_cie": d.codigo_cie,
                               "severidad": d.severidad}
                              for d in n.diagnosticos]}
            for n in notas
        ],
        "signos_vitales": signos,
        "valoraciones": valoraciones,
        "alertas_activas": alertas,
        "total_registros": len(notas) + len(signos) + len(valoraciones),
        "pagina_actual": pagina,
    }


@router.get("/{paciente_id}/alertas-activas")
async def get_alertas_activas(
    paciente_id: int,
    current_user=Depends(require_any),
):
    """Retorna alertas clínicas activas del paciente desde MongoDB."""
    val_col = get_valoraciones_collection()
    cursor = val_col.find(
        {"paciente_id": paciente_id, "requiere_intervencion": True},
        {"_id": 0}
    ).sort("timestamp", -1)
    alertas = await cursor.to_list(length=20)
    return {"paciente_id": paciente_id, "alertas": alertas, "total": len(alertas)}


@router.get("/{paciente_id}/tratamientos-activos")
def get_tratamientos_activos(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    """Retorna lista de medicamentos activos del paciente para chequeo de interacciones."""
    tratamientos = (
        db.query(MdTratamientos)
        .join(MdDiagnostico, MdTratamientos.diagnostico_id == MdDiagnostico.id)
        .join(MdNotasMedicas, MdDiagnostico.nota_id == MdNotasMedicas.id)
        .filter(
            MdNotasMedicas.paciente_id == paciente_id,
            MdTratamientos.activo == True,
        )
        .all()
    )
    return {"paciente_id": paciente_id, "tratamientos_activos": tratamientos}
