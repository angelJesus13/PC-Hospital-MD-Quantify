"""
config.py — Configuración centralizada de la aplicación
Carga variables desde .env usando pydantic-settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # Aplicación
    app_name: str = "Quantify Medical API"
    app_version: str = "2.0.0"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"

    # Base de datos SQL (MySQL)
    db_user: str = "root"
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "quantify_medical_db"
    db_pool_size: int = 20
    db_max_overflow: int = 40

    # Base de datos NoSQL (MongoDB)
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "quantify_nosql"
    mongo_logs_collection: str = "logs_auditoria"
    mongo_telemetria_collection: str = "telemetria_sesion"
    mongo_valoraciones_collection: str = "valoraciones_flexibles"

    # Seguridad JWT
    secret_key: str = "dev_secret_key_change_in_production_min_32_chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    refresh_token_expire_days: int = 7

    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"

    # Servidor
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            f"?charset=utf8mb4"
        )

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna instancia cacheada de configuración (singleton)."""
    return Settings()
