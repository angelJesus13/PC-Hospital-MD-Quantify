"""
schemas.py — Esquemas Pydantic v2 para validación y serialización
Cubre: Request bodies, Response models, y esquemas NoSQL
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Any, Dict
from datetime import datetime, date
from enum import Enum
import re


# ── Enumeraciones ─────────────────────────────────────────────────────────────

class RolSchema(str, Enum):
    admin = "admin"
    medico = "medico"
    enfermero = "enfermero"


class SexoSchema(str, Enum):
    M = "M"
    F = "F"
    NB = "NB"


class TipoNotaSchema(str, Enum):
    ingreso = "ingreso"
    evolucion = "evolucion"
    egreso = "egreso"
    interconsulta = "interconsulta"
    urgencias = "urgencias"


class SeveridadSchema(str, Enum):
    leve = "leve"
    moderado = "moderado"
    grave = "grave"
    critico = "critico"


class NivelSchema(str, Enum):
    NORMAL = "NORMAL"
    BAJO = "BAJO"
    MODERADO = "MODERADO"
    ALTO = "ALTO"
    CRITICO = "CRITICO"
    EMERGENCIA = "EMERGENCIA"


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    password: str = Field(..., min_length=6, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    usuario_id: int
    username: str
    role: RolSchema


class TokenData(BaseModel):
    usuario_id: int
    username: str
    role: RolSchema


# ── Usuarios ──────────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=80,
                          pattern=r'^[a-zA-Z0-9._-]+$')
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    role: RolSchema = RolSchema.medico


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[RolSchema] = None
    activo: Optional[bool] = None


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    role: RolSchema
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Pacientes ─────────────────────────────────────────────────────────────────

class PacienteCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    curp: str = Field(..., min_length=18, max_length=18)
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[SexoSchema] = None
    telefono: Optional[str] = Field(None, max_length=15)
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("curp")
    @classmethod
    def validar_curp(cls, v: str) -> str:
        patron = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$'
        if not re.match(patron, v.upper()):
            raise ValueError(
                "CURP inválida — debe tener formato oficial mexicano (18 caracteres)"
            )
        return v.upper()


class PacienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[SexoSchema] = None
    telefono: Optional[str] = Field(None, max_length=15)


class PacienteResponse(BaseModel):
    id: int
    nombre: str
    curp: str
    fecha_nacimiento: Optional[date]
    sexo: Optional[SexoSchema]
    telefono: Optional[str]
    fecha_registro: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class ExpedienteResponse(BaseModel):
    paciente: PacienteResponse
    notas_medicas: List[Any] = []
    diagnosticos: List[Any] = []
    tratamientos: List[Any] = []
    signos_vitales: List[Any] = []
    valoraciones: List[Any] = []
    alertas_activas: List[Any] = []
    total_registros: int = 0
    pagina_actual: int = 1


# ── Notas Médicas ─────────────────────────────────────────────────────────────

class NotaMedicaCreate(BaseModel):
    paciente_id: int = Field(..., gt=0)
    medico_id: int = Field(..., gt=0)
    contenido: str = Field(..., min_length=10)
    tipo_nota: TipoNotaSchema
    fecha: datetime = Field(default_factory=datetime.utcnow)


class NotaMedicaUpdate(BaseModel):
    contenido: Optional[str] = Field(None, min_length=10)
    tipo_nota: Optional[TipoNotaSchema] = None


class NotaMedicaResponse(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    contenido: str
    tipo_nota: TipoNotaSchema
    fecha: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Signos Vitales ────────────────────────────────────────────────────────────

class SignosVitalesCreate(BaseModel):
    paciente_id: int = Field(..., gt=0)
    tension_arterial: Optional[str] = Field(None, max_length=20,
                                             pattern=r'^\d{2,3}/\d{2,3}$')
    frecuencia_cardiaca: Optional[int] = Field(None, ge=0, le=300)
    temperatura: Optional[float] = Field(None, ge=30.0, le=45.0)
    frecuencia_respiratoria: Optional[int] = Field(None, ge=0, le=60)
    saturacion_o2: Optional[int] = Field(None, ge=0, le=100)
    escala_consciencia: Optional[str] = Field(None, max_length=30)
    fecha: datetime = Field(default_factory=datetime.utcnow)


class SignosVitalesResponse(BaseModel):
    id: int
    paciente_id: int
    tension_arterial: Optional[str]
    frecuencia_cardiaca: Optional[int]
    temperatura: Optional[float]
    frecuencia_respiratoria: Optional[int]
    saturacion_o2: Optional[int]
    escala_consciencia: Optional[str]
    score_mews: int
    fecha: datetime

    model_config = {"from_attributes": True}


# ── Diagnóstico ───────────────────────────────────────────────────────────────

class DiagnosticoCreate(BaseModel):
    nota_id: int = Field(..., gt=0)
    descripcion: str = Field(..., min_length=5)
    codigo_cie: Optional[str] = Field(None, max_length=7)
    severidad: SeveridadSchema = SeveridadSchema.leve

    @field_validator("codigo_cie")
    @classmethod
    def validar_cie10(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        patron = r'^[A-Z][0-9]{2}(\.[0-9]{1,2})?$'
        if not re.match(patron, v.upper()):
            raise ValueError(
                "Código CIE-10 inválido. Formato esperado: A99 o A99.9 (ej: J18.9)"
            )
        return v.upper()


class DiagnosticoResponse(BaseModel):
    id: int
    nota_id: int
    descripcion: str
    codigo_cie: Optional[str]
    severidad: SeveridadSchema
    activo: bool

    model_config = {"from_attributes": True}


# ── Tratamientos ──────────────────────────────────────────────────────────────

class TratamientoCreate(BaseModel):
    diagnostico_id: int = Field(..., gt=0)
    medicamento: str = Field(..., min_length=2, max_length=200)
    dosis: str = Field(..., min_length=1, max_length=50)
    frecuencia: str = Field(..., min_length=2, max_length=50)
    duracion: str = Field(..., min_length=1, max_length=30)
    fecha_inicio: Optional[datetime] = None
    forzar_prescripcion: bool = False  # Flag para override de interacciones


class TratamientoResponse(BaseModel):
    id: int
    diagnostico_id: int
    medicamento: str
    dosis: str
    frecuencia: str
    duracion: str
    activo: bool
    fecha_inicio: Optional[datetime]
    fecha_fin: Optional[datetime]

    model_config = {"from_attributes": True}


# ── Valoraciones ──────────────────────────────────────────────────────────────

class ValoracionCreate(BaseModel):
    paciente_id: int = Field(..., gt=0)
    escala: str = Field(..., pattern=r'^(Glasgow|MEWS|APGAR|Braden|Norton|SOFA)$')
    resultado: Optional[str] = Field(None, max_length=10)
    observaciones: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)
    registrado_por: Optional[int] = None
    # Datos extendidos para MongoDB
    componentes: Optional[Dict[str, Any]] = None


class ValoracionResponse(BaseModel):
    id: int
    paciente_id: int
    escala: str
    resultado: Optional[str]
    observaciones: Optional[str]
    fecha: datetime

    model_config = {"from_attributes": True}


# ── Domicilios ────────────────────────────────────────────────────────────────

class DomicilioCreate(BaseModel):
    calle: str = Field(..., min_length=3, max_length=200)
    colonia: str = Field(..., min_length=2, max_length=100)
    municipio: str = Field(..., min_length=2, max_length=100)
    estado: str = Field(..., min_length=2, max_length=60)
    cp: str = Field(..., pattern=r'^\d{5}$')
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)
    tipo_domicilio: str = "principal"


class DomicilioResponse(BaseModel):
    id: int
    calle: str
    colonia: str
    municipio: str
    estado: str
    cp: str
    latitud: Optional[float]
    longitud: Optional[float]

    model_config = {"from_attributes": True}


# ── NoSQL — Logs Auditoría ────────────────────────────────────────────────────

class LogAuditoriaCreate(BaseModel):
    usuario_id: int
    username: str
    ip_address: str
    accion: str
    entidad_afectada: Optional[Dict[str, Any]] = None
    cambios: Optional[Dict[str, Any]] = None
    resultado: str = "EXITO"
    codigo_http: Optional[int] = None
    mensaje_error: Optional[str] = None
    nivel: str = "INFO"
    correlacion_id: Optional[str] = None
    user_agent: Optional[str] = None


# ── NoSQL — Telemetría ────────────────────────────────────────────────────────

class TelemetriaCreate(BaseModel):
    token_jti: str
    usuario_id: int
    username: str
    rol: RolSchema
    ip_address: str
    turno: Optional[str] = None
    area_clinica: Optional[str] = None


# ── NoSQL — Valoraciones Flexibles ───────────────────────────────────────────

class ValoracionFlexibleCreate(BaseModel):
    paciente_id: int
    valoracion_sql_id: Optional[int] = None
    registrado_por_id: Optional[int] = None
    tipo: str
    nivel: NivelSchema
    componentes: Optional[Dict[str, Any]] = None
    total: Optional[float] = None
    interpretacion: Optional[str] = None
    requiere_intervencion: bool = False
    accion_tomada: Optional[str] = None
    notificado: bool = False


# ── Reportes ──────────────────────────────────────────────────────────────────

class EpidemiologiaResponse(BaseModel):
    municipio: str
    colonia: str
    casos: int


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    pagina: int
    limite: int
    paginas_totales: int
