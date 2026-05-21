"""
database.py — Configuración de SQLAlchemy para MySQL
Motor híbrido: sesión sync para operaciones CRUD + async ready
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
from config import get_settings

settings = get_settings()

# ── Engine con connection pooling configurado para entorno hospitalario ──
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=settings.db_pool_size,       # Conexiones permanentes
    max_overflow=settings.db_max_overflow,  # Conexiones extra bajo carga
    pool_pre_ping=True,                     # Verifica conexión antes de usar
    pool_recycle=3600,                      # Recicla conexiones cada 1 hora
    echo=settings.debug,                    # SQL logging en modo debug
    connect_args={
        "charset": "utf8mb4",
        "connect_timeout": 10,
    },
)

# ── Sesión ──
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── Base para todos los modelos ORM ──
Base = declarative_base()


# ── Dependencia FastAPI ──
def get_db() -> Generator[Session, None, None]:
    """
    Proveedor de sesión de base de datos para inyección de dependencias FastAPI.
    Garantiza cierre de sesión aunque ocurra una excepción.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Crea todas las tablas si no existen. Solo para desarrollo/testing."""
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """Elimina todas las tablas. PELIGROSO — solo para testing."""
    Base.metadata.drop_all(bind=engine)
