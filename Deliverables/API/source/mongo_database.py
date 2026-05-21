"""
mongo_database.py — Configuración de Motor (MongoDB async)
Colecciones: logs_auditoria, telemetria_sesion, valoraciones_flexibles
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING, IndexModel
from config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Cliente Motor global ──
_mongo_client: AsyncIOMotorClient | None = None
_mongo_db: AsyncIOMotorDatabase | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(
            settings.mongo_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            maxPoolSize=50,
            minPoolSize=5,
        )
    return _mongo_client


def get_mongo_db() -> AsyncIOMotorDatabase:
    global _mongo_db
    if _mongo_db is None:
        _mongo_db = get_mongo_client()[settings.mongo_db]
    return _mongo_db


# ── Colecciones — acceso directo ──
def get_logs_collection():
    return get_mongo_db()[settings.mongo_logs_collection]


def get_telemetria_collection():
    return get_mongo_db()[settings.mongo_telemetria_collection]


def get_valoraciones_collection():
    return get_mongo_db()[settings.mongo_valoraciones_collection]


# ── Inicialización de índices ──
async def init_mongo_indexes() -> None:
    """Crea todos los índices necesarios al iniciar la aplicación."""
    db = get_mongo_db()

    # logs_auditoria
    logs = db[settings.mongo_logs_collection]
    await logs.create_indexes([
        IndexModel([("timestamp", DESCENDING)]),
        IndexModel([("usuario_id", ASCENDING), ("timestamp", DESCENDING)]),
        IndexModel([("accion", ASCENDING)]),
        IndexModel([("nivel", ASCENDING)]),
        IndexModel([
            ("entidad_afectada.tipo", ASCENDING),
            ("entidad_afectada.id", ASCENDING),
        ]),
        IndexModel([("correlacion_id", ASCENDING)], unique=True, sparse=True),
    ])

    # telemetria_sesion
    telemetria = db[settings.mongo_telemetria_collection]
    await telemetria.create_indexes([
        IndexModel([("token_jti", ASCENDING)], unique=True),
        IndexModel([("usuario_id", ASCENDING), ("inicio_sesion", DESCENDING)]),
        IndexModel([("estado", ASCENDING)]),
        IndexModel([("inicio_sesion", DESCENDING)]),
        IndexModel([("turno", ASCENDING), ("area_clinica", ASCENDING)]),
    ])

    # valoraciones_flexibles
    valoraciones = db[settings.mongo_valoraciones_collection]
    await valoraciones.create_indexes([
        IndexModel([("paciente_id", ASCENDING), ("timestamp", DESCENDING)]),
        IndexModel([("tipo", ASCENDING)]),
        IndexModel([("nivel", ASCENDING)]),
        IndexModel([("timestamp", DESCENDING)]),
        IndexModel([("requiere_intervencion", ASCENDING)]),
        IndexModel([("expira_en", ASCENDING)], expireAfterSeconds=0),  # TTL
    ])

    logger.info("MongoDB indexes initialized successfully.")


async def close_mongo_connection() -> None:
    """Cierra la conexión MongoDB al apagar la aplicación."""
    global _mongo_client, _mongo_db
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _mongo_db = None
        logger.info("MongoDB connection closed.")
