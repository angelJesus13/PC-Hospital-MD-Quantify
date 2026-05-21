"""routes/auditoria.py — Consulta de logs de auditoría (MongoDB)"""
from fastapi import APIRouter, Depends, Query
from auth import require_admin, require_any
from mongo_database import get_logs_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/auditoria", tags=["Auditoría"])


@router.get("/")
async def get_logs(
    current_user=Depends(require_admin),
    accion: str = Query(None),
    usuario_id: int = Query(None),
    nivel: str = Query(None),
    fecha: str = Query(None, description="Fecha en formato YYYY-MM-DD"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(50, ge=1, le=200),
):
    """Consulta logs de auditoría con filtros. Solo accesible por admin."""
    logs = get_logs_collection()
    filtro: dict = {}

    if accion:
        filtro["accion"] = accion.upper()
    if usuario_id:
        filtro["usuario_id"] = usuario_id
    if nivel:
        filtro["nivel"] = nivel.upper()
    if fecha:
        try:
            dt = datetime.strptime(fecha, "%Y-%m-%d")
            filtro["timestamp"] = {
                "$gte": dt.replace(tzinfo=timezone.utc),
                "$lt": dt.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc),
            }
        except ValueError:
            pass

    total = await logs.count_documents(filtro)
    skip = (pagina - 1) * limite
    cursor = logs.find(filtro, {"_id": 0}).sort("timestamp", -1).skip(skip).limit(limite)
    items = await cursor.to_list(length=limite)

    return {
        "logs": items,
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "paginas_totales": max(1, (total + limite - 1) // limite),
    }


@router.get("/emergencias")
async def get_emergencias(current_user=Depends(require_any)):
    """Retorna los últimos 20 eventos de nivel EMERGENCIA."""
    logs = get_logs_collection()
    cursor = logs.find(
        {"nivel": "EMERGENCIA"}, {"_id": 0}
    ).sort("timestamp", -1).limit(20)
    emergencias = await cursor.to_list(length=20)
    return {"emergencias": emergencias, "total": len(emergencias)}


@router.get("/estadisticas")
async def get_estadisticas(current_user=Depends(require_admin)):
    """Retorna estadísticas de actividad del sistema."""
    logs = get_logs_collection()
    pipeline = [
        {"$group": {
            "_id": "$accion",
            "total": {"$sum": 1},
            "ultimo": {"$max": "$timestamp"},
        }},
        {"$sort": {"total": -1}},
    ]
    cursor = logs.aggregate(pipeline)
    stats = await cursor.to_list(length=50)
    return {"estadisticas_por_accion": stats}
