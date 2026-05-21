"""
main.py — Entry point de la API Híbrida Quantify Medical
FastAPI + SQLAlchemy (MySQL) + Motor (MongoDB)
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from config import get_settings
from database import create_tables
from mongo_database import init_mongo_indexes, close_mongo_connection
import logging

# ── Importar routers ──────────────────────────────────────────────────────────
from routes.usuarios import router as usuarios_router, auth_router
from routes.pacientes import router as pacientes_router
from routes.notas_medicas import router as notas_router
from routes.signos_vitales import router as signos_router
from routes.diagnostico import router as dx_router
from routes.tratamientos import router as tx_router
from routes.valoraciones import router as val_router
from routes.auditoria import router as auditoria_router
from routes.telemetria import router as telemetria_router

settings = get_settings()
logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando Quantify Medical API v%s...", settings.app_version)

    # SQL: crear tablas si no existen (usar Alembic en producción)
    if settings.app_env == "development":
        create_tables()
        logger.info("✅ Tablas SQL verificadas/creadas.")

    # MongoDB: inicializar índices
    await init_mongo_indexes()
    logger.info("✅ Índices MongoDB inicializados.")

    yield  # ── Aplicación corriendo ──

    # Shutdown
    await close_mongo_connection()
    logger.info("🛑 Conexión MongoDB cerrada. API detenida.")


# ── Instancia FastAPI ─────────────────────────────────────────────────────────
app = FastAPI(
    title="Quantify Medical Hybrid API",
    description=(
        "API REST híbrida (SQL + NoSQL) para gestión de expedientes clínicos. "
        "Proyecto: PC-Hospital-MD-Quantify | UDN Simulation Tests"
    ),
    version=settings.app_version,
    contact={
        "name": "Angel de Jesús — Tech Lead",
        "url": "https://github.com/angelJesus13",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

# ── Middleware CORS ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Manejador global de excepciones ──────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Contacte al administrador."},
    )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
async def health_check():
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.app_env,
    }


# ── Registrar routers ─────────────────────────────────────────────────────────
prefix = settings.api_prefix

app.include_router(auth_router, prefix=prefix)
app.include_router(usuarios_router, prefix=prefix)
app.include_router(pacientes_router, prefix=prefix)
app.include_router(notas_router, prefix=prefix)
app.include_router(signos_router, prefix=prefix)
app.include_router(dx_router, prefix=prefix)
app.include_router(tx_router, prefix=prefix)
app.include_router(val_router, prefix=prefix)
app.include_router(auditoria_router, prefix=prefix)
app.include_router(telemetria_router, prefix=prefix)


# ── Punto de entrada directo ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers,
        log_level="debug" if settings.debug else "info",
    )
