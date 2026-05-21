"""
models.py — Modelos ORM SQLAlchemy
Mapea las 12 tablas MySQL del sistema clínico Quantify
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, DateTime,
    DECIMAL, CHAR, Enum, ForeignKey, Index, CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# ── Enumeraciones Python ──────────────────────────────────────────────────────

class RolEnum(str, enum.Enum):
    admin = "admin"
    medico = "medico"
    enfermero = "enfermero"


class SexoEnum(str, enum.Enum):
    M = "M"
    F = "F"
    NB = "NB"


class TipoNotaEnum(str, enum.Enum):
    ingreso = "ingreso"
    evolucion = "evolucion"
    egreso = "egreso"
    interconsulta = "interconsulta"
    urgencias = "urgencias"


class SeveridadEnum(str, enum.Enum):
    leve = "leve"
    moderado = "moderado"
    grave = "grave"
    critico = "critico"


class TipoDocumentoEnum(str, enum.Enum):
    ine = "ine"
    curp = "curp"
    nss = "nss"
    pasaporte = "pasaporte"
    acta_nacimiento = "acta_nacimiento"


class TipoDomicilioEnum(str, enum.Enum):
    principal = "principal"
    temporal = "temporal"
    referencia = "referencia"


# ── Modelos ORM ──────────────────────────────────────────────────────────────

class MdUsuarios(Base):
    """Usuarios del sistema clínico con autenticación JWT y roles."""
    __tablename__ = "md_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    role = Column(Enum(RolEnum), nullable=False, default=RolEnum.medico)
    activo = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relaciones
    notas_medicas = relationship("MdNotasMedicas", back_populates="medico",
                                 foreign_keys="MdNotasMedicas.medico_id")
    valoraciones_registradas = relationship("MdValoraciones",
                                            back_populates="registrado_por_usuario",
                                            foreign_keys="MdValoraciones.registrado_por")

    __table_args__ = (
        Index("idx_usuarios_role", "role"),
    )


class MdPacientes(Base):
    """Registro maestro de pacientes — entidad central del sistema."""
    __tablename__ = "md_pacientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    curp = Column(CHAR(18), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=True)
    sexo = Column(Enum(SexoEnum), nullable=True)
    telefono = Column(String(15), nullable=True)
    fecha_registro = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relaciones
    notas_medicas = relationship("MdNotasMedicas", back_populates="paciente",
                                 cascade="all, delete-orphan")
    signos_vitales = relationship("MdSignosVitales", back_populates="paciente",
                                  cascade="all, delete-orphan")
    valoraciones = relationship("MdValoraciones", back_populates="paciente",
                                cascade="all, delete-orphan")
    documentos_oficiales = relationship("MdDocumentosOficiales",
                                        back_populates="paciente",
                                        cascade="all, delete-orphan")
    nacimiento = relationship("MdNacimientos", back_populates="paciente",
                              uselist=False)
    defuncion = relationship("MdDefunciones", back_populates="paciente",
                             uselist=False)
    domicilios = relationship("MdPersonasTieneDomicilio", back_populates="paciente",
                              cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_pacientes_nombre", "nombre"),
        Index("idx_pacientes_fecha_registro", "fecha_registro"),
    )


class MdNotasMedicas(Base):
    """Notas clínicas — historial de episodios médicos."""
    __tablename__ = "md_notas_medicas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="CASCADE"),
                         nullable=False)
    medico_id = Column(Integer, ForeignKey("md_usuarios.id", ondelete="RESTRICT"),
                       nullable=False)
    contenido = Column(Text, nullable=False)
    tipo_nota = Column(Enum(TipoNotaEnum), nullable=False)
    fecha = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="notas_medicas")
    medico = relationship("MdUsuarios", back_populates="notas_medicas",
                          foreign_keys=[medico_id])
    diagnosticos = relationship("MdDiagnostico", back_populates="nota_medica",
                                cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_notas_paciente_fecha", "paciente_id", "fecha"),
        Index("idx_notas_medico", "medico_id"),
        Index("idx_notas_tipo", "tipo_nota"),
    )


class MdSignosVitales(Base):
    """Parámetros fisiológicos medidos por enfermería."""
    __tablename__ = "md_signos_vitales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="CASCADE"),
                         nullable=False)
    tension_arterial = Column(String(20), nullable=True)
    frecuencia_cardiaca = Column(Integer, nullable=True)
    temperatura = Column(DECIMAL(5, 2), nullable=True)
    frecuencia_respiratoria = Column(Integer, nullable=True)
    saturacion_o2 = Column(Integer, nullable=True)
    escala_consciencia = Column(String(30), nullable=True)
    score_mews = Column(Integer, nullable=False, default=0)
    fecha = Column(DateTime, nullable=False)

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="signos_vitales")

    __table_args__ = (
        Index("idx_sv_paciente_fecha", "paciente_id", "fecha"),
        Index("idx_sv_score_mews", "score_mews"),
        CheckConstraint("frecuencia_cardiaca BETWEEN 0 AND 300",
                        name="chk_sv_fc"),
        CheckConstraint("temperatura BETWEEN 30.0 AND 45.0",
                        name="chk_sv_temp"),
        CheckConstraint("saturacion_o2 BETWEEN 0 AND 100",
                        name="chk_sv_spo2"),
        CheckConstraint("frecuencia_respiratoria BETWEEN 0 AND 60",
                        name="chk_sv_fr"),
    )


class MdDiagnostico(Base):
    """Diagnósticos médicos con codificación CIE-10."""
    __tablename__ = "md_diagnostico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nota_id = Column(Integer, ForeignKey("md_notas_medicas.id", ondelete="CASCADE"),
                     nullable=False)
    descripcion = Column(Text, nullable=False)
    codigo_cie = Column(CHAR(7), nullable=True)
    severidad = Column(Enum(SeveridadEnum), nullable=False, default=SeveridadEnum.leve)
    activo = Column(Boolean, nullable=False, default=True)

    # Relaciones
    nota_medica = relationship("MdNotasMedicas", back_populates="diagnosticos")
    tratamientos = relationship("MdTratamientos", back_populates="diagnostico",
                                cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_dx_nota", "nota_id"),
        Index("idx_dx_codigo_cie", "codigo_cie"),
        Index("idx_dx_severidad", "severidad"),
    )


class MdTratamientos(Base):
    """Prescripciones médicas vinculadas a un diagnóstico."""
    __tablename__ = "md_tratamientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    diagnostico_id = Column(Integer, ForeignKey("md_diagnostico.id",
                                                 ondelete="CASCADE"), nullable=False)
    medicamento = Column(String(200), nullable=False)
    dosis = Column(String(50), nullable=False)
    frecuencia = Column(String(50), nullable=False)
    duracion = Column(String(30), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)

    # Relaciones
    diagnostico = relationship("MdDiagnostico", back_populates="tratamientos")

    __table_args__ = (
        Index("idx_tx_diagnostico", "diagnostico_id"),
        Index("idx_tx_activo", "activo"),
        Index("idx_tx_medicamento", "medicamento"),
    )


class MdNacimientos(Base):
    """Datos de nacimiento — relación 1:1 con md_pacientes."""
    __tablename__ = "md_nacimientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="RESTRICT"),
                         nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    lugar = Column(String(200), nullable=False)
    nombre_madre = Column(String(100), nullable=True)
    nombre_padre = Column(String(100), nullable=True)
    peso_al_nacer = Column(DECIMAL(5, 2), nullable=True)
    talla_al_nacer = Column(DECIMAL(5, 2), nullable=True)

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="nacimiento")


class MdDefunciones(Base):
    """Registro de defunciones hospitalarias — relación 1:0..1 con md_pacientes."""
    __tablename__ = "md_defunciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="RESTRICT"),
                         nullable=False, unique=True)
    fecha_defuncion = Column(DateTime, nullable=False)
    causa = Column(Text, nullable=False)
    causa_basica = Column(Text, nullable=True)
    certificador = Column(String(50), nullable=True)

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="defuncion")

    __table_args__ = (
        Index("idx_def_fecha", "fecha_defuncion"),
    )


class MdDocumentosOficiales(Base):
    """Documentos de identidad del paciente."""
    __tablename__ = "md_documentos_oficiales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="CASCADE"),
                         nullable=False)
    tipo_documento = Column(Enum(TipoDocumentoEnum), nullable=False)
    numero_documento = Column(String(60), nullable=False)
    fecha_emision = Column(Date, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    vigente = Column(Boolean, nullable=False, default=True)

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="documentos_oficiales")

    __table_args__ = (
        Index("idx_docs_paciente", "paciente_id"),
        Index("idx_docs_tipo", "tipo_documento"),
        UniqueConstraint("tipo_documento", "numero_documento", name="uq_docs_numero"),
    )


class MdDomicilios(Base):
    """Catálogo de domicilios con coordenadas GPS."""
    __tablename__ = "md_domicilios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    calle = Column(String(200), nullable=False)
    colonia = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    estado = Column(String(60), nullable=False)
    cp = Column(CHAR(5), nullable=False)
    latitud = Column(DECIMAL(10, 7), nullable=True)
    longitud = Column(DECIMAL(10, 7), nullable=True)

    # Relaciones
    residentes = relationship("MdPersonasTieneDomicilio", back_populates="domicilio")

    __table_args__ = (
        Index("idx_dom_municipio", "municipio"),
        Index("idx_dom_estado", "estado"),
        Index("idx_dom_cp", "cp"),
    )


class MdPersonasTieneDomicilio(Base):
    """Tabla intermedia N:M entre pacientes y domicilios."""
    __tablename__ = "md_personas_tiene_domicilio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="CASCADE"),
                         nullable=False)
    domicilio_id = Column(Integer, ForeignKey("md_domicilios.id", ondelete="CASCADE"),
                          nullable=False)
    tipo_domicilio = Column(Enum(TipoDomicilioEnum), nullable=False,
                            default=TipoDomicilioEnum.principal)
    activo = Column(Boolean, nullable=False, default=True)

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="domicilios")
    domicilio = relationship("MdDomicilios", back_populates="residentes")

    __table_args__ = (
        UniqueConstraint("paciente_id", "domicilio_id", "tipo_domicilio",
                         name="uq_ptd_unique"),
        Index("idx_ptd_paciente", "paciente_id"),
        Index("idx_ptd_domicilio", "domicilio_id"),
    )


class MdValoraciones(Base):
    """Escalas clínicas estandarizadas — resumen en SQL, detalle en MongoDB."""
    __tablename__ = "md_valoraciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("md_pacientes.id", ondelete="CASCADE"),
                         nullable=False)
    escala = Column(String(50), nullable=False)
    resultado = Column(String(10), nullable=True)
    observaciones = Column(Text, nullable=True)
    fecha = Column(DateTime, nullable=False)
    registrado_por = Column(Integer, ForeignKey("md_usuarios.id",
                                                 ondelete="SET NULL"), nullable=True)

    # Relaciones
    paciente = relationship("MdPacientes", back_populates="valoraciones")
    registrado_por_usuario = relationship("MdUsuarios",
                                          back_populates="valoraciones_registradas",
                                          foreign_keys=[registrado_por])

    __table_args__ = (
        Index("idx_val_paciente_fecha", "paciente_id", "fecha"),
        Index("idx_val_escala", "escala"),
        CheckConstraint(
            "escala IN ('Glasgow','MEWS','APGAR','Braden','Norton','SOFA')",
            name="chk_val_escala"
        ),
    )
