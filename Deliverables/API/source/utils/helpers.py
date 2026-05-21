"""utils/helpers.py — Funciones auxiliares del sistema"""
from datetime import datetime, timezone
from typing import Optional


# ── Score MEWS ────────────────────────────────────────────────────────────────

def calcular_mews(
    frecuencia_cardiaca: Optional[int] = None,
    frecuencia_respiratoria: Optional[int] = None,
    saturacion_o2: Optional[int] = None,
    temperatura: Optional[float] = None,
    escala_consciencia: Optional[str] = None,
) -> tuple[int, str]:
    """
    Calcula el score MEWS (Modified Early Warning Score).
    Retorna (score, nivel_clasificacion).
    """
    score = 0
    parametros_criticos = []

    # Frecuencia cardíaca
    if frecuencia_cardiaca is not None:
        if frecuencia_cardiaca < 40 or frecuencia_cardiaca > 130:
            score += 2
            parametros_criticos.append(f"FC={frecuencia_cardiaca} lpm")
        elif frecuencia_cardiaca < 50 or frecuencia_cardiaca > 110:
            score += 1

    # Frecuencia respiratoria
    if frecuencia_respiratoria is not None:
        if frecuencia_respiratoria < 9 or frecuencia_respiratoria > 30:
            score += 3
            parametros_criticos.append(f"FR={frecuencia_respiratoria} rpm")
        elif frecuencia_respiratoria > 20:
            score += 1

    # Saturación O2
    if saturacion_o2 is not None:
        if saturacion_o2 < 85:
            score += 3
            parametros_criticos.append(f"SpO2={saturacion_o2}%")
        elif saturacion_o2 < 90:
            score += 2
        elif saturacion_o2 < 95:
            score += 1

    # Temperatura
    if temperatura is not None:
        if temperatura < 35.0 or temperatura > 39.0:
            score += 2
            parametros_criticos.append(f"Temp={temperatura}°C")
        elif temperatura < 36.0 or temperatura > 38.5:
            score += 1

    # Nivel de consciencia
    if escala_consciencia:
        ec = escala_consciencia.lower()
        if "inconsciente" in ec or "coma" in ec:
            score += 3
            parametros_criticos.append("Consciencia: inconsciente")
        elif "confuso" in ec or "somnoliento" in ec:
            score += 2
        elif "desorientado" in ec:
            score += 1

    # Clasificación
    if score <= 4:
        nivel = "NORMAL"
    elif score <= 6:
        nivel = "MODERADO"
    else:
        nivel = "CRITICO"

    return score, nivel


def clasificar_glasgow(total: int) -> str:
    """Clasifica el nivel de consciencia según escala Glasgow."""
    if total >= 13:
        return "Leve"
    elif total >= 9:
        return "Moderado"
    else:
        return "Grave"


def get_turno_actual() -> str:
    """Determina el turno clínico según la hora actual."""
    hora = datetime.now(timezone.utc).hour
    if 7 <= hora < 15:
        return "matutino"
    elif 15 <= hora < 23:
        return "vespertino"
    else:
        return "nocturno"


def paginar(query, pagina: int, limite: int):
    """Aplica paginación a un query SQLAlchemy."""
    offset = (pagina - 1) * limite
    total = query.count()
    items = query.offset(offset).limit(limite).all()
    return items, total


def calcular_paginas(total: int, limite: int) -> int:
    """Calcula el número total de páginas."""
    return max(1, (total + limite - 1) // limite)
