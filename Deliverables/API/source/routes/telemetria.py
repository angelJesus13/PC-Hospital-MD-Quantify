"""routes/telemetria.py — Consulta de telemetría de sesiones (MongoDB)"""
from fastapi import APIRouter, Depends, Query
from auth import require_admin, require_any
from mongo_database import get_telemetria_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/telemetria", tags=["Telemetría"])


@router.get("/sesiones")
async def get_sesiones(
    current_user=Depends(require_admin),
    usuario_id: int = Query(None),
    estado: str = Query(None),
    turno: str = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(50, ge=1, le=100),
):
    """Consulta sesiones de usuario con métricas de uso."""
    tel = get_telemetria_collection()
    filtro: dict = {}
    if usuario_id:
        filtro["usuario_id"] = usuario_id
    if estado:
        filtro["estado"] = estado.lower()
    if turno:
        filtro["turno"] = turno.lower()

    total = await tel.count_documents(filtro)
    skip = (pagina - 1) * limite
    cursor = tel.find(filtro, {"_id": 0}).sort("inicio_sesion", -1).skip(skip).limit(limite)
    items = await cursor.to_list(length=limite)

    return {
        "sesiones": items,
        "total": total,
        "pagina": pagina,
        "limite": limite,
    }


@router.get("/sesiones-activas")
async def get_sesiones_activas(current_user=Depends(require_admin)):
    """Retorna todas las sesiones JWT actualmente activas."""
    tel = get_telemetria_collection()
    cursor = tel.find({"estado": "activa"}, {"_id": 0}).sort("inicio_sesion", -1)
    sesiones = await cursor.to_list(length=100)
    return {"sesiones_activas": sesiones, "total": len(sesiones)}


@router.get("/uso-por-turno")
async def uso_por_turno(current_user=Depends(require_admin)):
    """Estadísticas de uso agrupadas por turno clínico."""
    tel = get_telemetria_collection()
    pipeline = [
        {"$match": {"turno": {"$ne": None}}},
        {"$group": {
            "_id": "$turno",
            "sesiones": {"$sum": 1},
            "requests_totales": {"$sum": "$requests_totales"},
            "duracion_promedio_seg": {"$avg": "$duracion_segundos"},
        }},
        {"$sort": {"sesiones": -1}},
    ]
    cursor = tel.aggregate(pipeline)
    stats = await cursor.to_list(length=10)
    return {"uso_por_turno": stats}


@router.get("/endpoints-mas-usados")
async def endpoints_mas_usados(current_user=Depends(require_admin)):
    """Top 10 endpoints más invocados en el sistema."""
    tel = get_telemetria_collection()
    pipeline = [
        {"$unwind": "$endpoints_visitados"},
        {"$group": {
            "_id": "$endpoints_visitados.endpoint",
            "total_llamadas": {"$sum": "$endpoints_visitados.conteo"},
            "latencia_promedio_ms": {"$avg": "$endpoints_visitados.latencia_promedio_ms"},
        }},
        {"$sort": {"total_llamadas": -1}},
        {"$limit": 10},
    ]
    cursor = tel.aggregate(pipeline)
    stats = await cursor.to_list(length=10)
    return {"endpoints_mas_usados": stats}
