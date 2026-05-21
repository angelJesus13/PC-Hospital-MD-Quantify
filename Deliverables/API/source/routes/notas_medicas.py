"""routes/notas_medicas.py — CRUD de notas clínicas"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models import MdNotasMedicas, MdPacientes, MdUsuarios
from schemas import NotaMedicaCreate, NotaMedicaUpdate, NotaMedicaResponse
from auth import require_any, require_medico, get_current_user
from mongo_database import get_logs_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/notas-medicas", tags=["Notas Médicas"])


@router.post("/", response_model=NotaMedicaResponse, status_code=status.HTTP_201_CREATED)
async def create_nota(
    data: NotaMedicaCreate,
    db: Session = Depends(get_db),
    current_user: MdUsuarios = Depends(require_medico),
):
    # Verificar existencia de paciente y médico
    if not db.query(MdPacientes).filter(MdPacientes.id == data.paciente_id).first():
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    if not db.query(MdUsuarios).filter(MdUsuarios.id == data.medico_id).first():
        raise HTTPException(status_code=404, detail="Médico no encontrado")

    nota = MdNotasMedicas(**data.model_dump())
    db.add(nota)
    db.commit()
    db.refresh(nota)

    logs = get_logs_collection()
    await logs.insert_one({
        "usuario_id": current_user.id, "username": current_user.username,
        "ip_address": "system", "accion": "CREATE_NOTA",
        "entidad_afectada": {"tipo": "nota_medica", "id": nota.id,
                              "tabla": "md_notas_medicas"},
        "cambios": {"antes": None, "despues": {
            "paciente_id": data.paciente_id,
            "tipo_nota": data.tipo_nota.value,
        }},
        "resultado": "EXITO", "codigo_http": 201, "nivel": "INFO",
        "timestamp": datetime.now(timezone.utc),
    })
    return nota


@router.get("/", response_model=list[NotaMedicaResponse])
def list_notas(
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
    paciente_id: int = Query(None),
    medico_id: int = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
):
    query = db.query(MdNotasMedicas).order_by(MdNotasMedicas.fecha.desc())
    if paciente_id:
        query = query.filter(MdNotasMedicas.paciente_id == paciente_id)
    if medico_id:
        query = query.filter(MdNotasMedicas.medico_id == medico_id)
    offset = (pagina - 1) * limite
    return query.offset(offset).limit(limite).all()


@router.get("/{nota_id}", response_model=NotaMedicaResponse)
def get_nota(
    nota_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any),
):
    nota = db.query(MdNotasMedicas).filter(MdNotasMedicas.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota médica no encontrada")
    return nota


@router.put("/{nota_id}", response_model=NotaMedicaResponse)
def update_nota(
    nota_id: int,
    data: NotaMedicaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_medico),
):
    nota = db.query(MdNotasMedicas).filter(MdNotasMedicas.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota médica no encontrada")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(nota, field, value)
    db.commit()
    db.refresh(nota)
    return nota
