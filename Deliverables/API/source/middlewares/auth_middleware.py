"""middlewares/auth_middleware.py — Logging de requests para telemetría"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from mongo_database import get_telemetria_collection
from datetime import datetime, timezone
import time


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que registra métricas de cada request para telemetría.
    Actualiza `endpoints_visitados` en la colección MongoDB.
    """

    SKIP_PATHS = {"/health", "/api/v1/docs", "/api/v1/redoc",
                  "/api/v1/openapi.json"}

    async def dispatch(self, request: Request, call_next) -> Response:
        # Saltar rutas de sistema
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        start_time = time.monotonic()
        response = await call_next(request)
        duration_ms = (time.monotonic() - start_time) * 1000

        # Obtener JTI del token (si hay Authorization header)
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from auth import decode_token
                token_data = decode_token(auth_header[7:])
                endpoint_key = f"{request.method} {request.url.path}"

                tel = get_telemetria_collection()
                await tel.update_one(
                    {"usuario_id": token_data.usuario_id, "estado": "activa"},
                    {
                        "$inc": {"requests_totales": 1},
                        "$push": {
                            "endpoints_visitados": {
                                "endpoint": endpoint_key,
                                "metodo": request.method,
                                "conteo": 1,
                                "latencia_ms": round(duration_ms, 2),
                                "timestamp": datetime.now(timezone.utc),
                                "status_code": response.status_code,
                            }
                        },
                        "$set": {"updatedAt": datetime.now(timezone.utc)},
                    },
                    sort=[("inicio_sesion", -1)],
                )
            except Exception:
                pass  # No fallar si la telemetría falla

        return response
