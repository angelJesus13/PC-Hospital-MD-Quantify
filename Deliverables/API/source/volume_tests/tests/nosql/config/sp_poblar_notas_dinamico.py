"""
Equivalente Python de sp_poblar_notas_dinamico.sql para MongoDB.
Orquestador principal que genera N documentos de notas médicas 
llamando a las 6 funciones modulares e insertándolos en MongoDB en batch.
"""
import random
from datetime import datetime, timedelta

from tests.nosql.config.fn_generar_antecedentes import fn_generar_antecedentes
from tests.nosql.config.fn_generar_auditoria import fn_generar_auditoria
from tests.nosql.config.fn_generar_interrogatorio import fn_generar_interrogatorio
from tests.nosql.config.fn_generar_signos_vitales import fn_generar_signos_vitales
from tests.nosql.config.fn_generar_sintomas import fn_generar_sintomas
from tests.nosql.config.fn_generar_tipo_nota import fn_generar_tipo_nota
from config.db_mongo import get_mongo_db, log_bitacora_mongo


def sp_poblar_notas_dinamico(
    p_cantidad: int,
    p_tipos_nota: list[str],
    p_pediatria: bool,
    p_uci: bool,
    p_zero: bool,
    p_usuario_ip: str,
    ids_pacientes: list[int],
    ids_medicos: list[int],
    ids_expedientes: list[int]
) -> dict:
    """
    Replica del Stored Procedure sp_poblar_notas_dinamico de MySQL,
    adaptado para MongoDB usando las funciones Python modulares.
    
    A diferencia del SQL que inserta fila por fila con COMMIT cada 5000,
    aquí usamos insert_many en batch de 10000 (eficiencia MongoDB).
    
    Args:
        p_cantidad: Número de documentos a generar.
        p_tipos_nota: Lista de tipos de nota permitidos (ej: ["Ingreso", "Evolución"]).
        p_pediatria: Si se incluyen casos pediátricos.
        p_uci: Si se incluyen casos UCI.
        p_zero: Si se incluyen pacientes zero (desconocidos).
        p_usuario_ip: IP del usuario que lanza la prueba.
        ids_pacientes: Lista de IDs de pacientes válidos (de MySQL).
        ids_medicos: Lista de IDs de médicos válidos (de MySQL).
        ids_expedientes: Lista de IDs de expedientes válidos (de MySQL).
        
    Returns:
        Dict con resumen de la operación.
    """
    if p_cantidad is None or p_cantidad <= 0:
        raise ValueError("Error: la cantidad debe ser mayor a 0.")

    db = get_mongo_db()
    coleccion = db["NotasMedicas"]

    batch_size = 10000
    insertados = 0
    notas_batch = []

    for i in range(p_cantidad):
        # --- Escoger tipo de nota del array inyectado (como el CSV del SQL) ---
        v_tipo_nota = random.choice(p_tipos_nota)

        # --- Determinar si es paciente zero ---
        v_es_zero = p_zero

        # --- Asegurar IDs reales para las llaves foráneas ---
        v_medico_id = random.choice(ids_medicos)
        v_paciente_id = random.choice(ids_pacientes)
        v_expediente_id = v_paciente_id  # Amarrado 1 a 1 como en MySQL

        # --- Edad según pediatría ---
        if p_pediatria:
            v_edad = random.randint(1, 14)
        else:
            v_edad = random.randint(18, 77)

        # --- Género aleatorio ---
        v_genero = 'hombre' if random.random() < 0.5 else 'mujer'

        # --- Fecha de registro aleatoria del último año ---
        v_fecha_reg = datetime.utcnow() - timedelta(days=random.randint(0, 365))

        # --- Llamar las 6 funciones modulares (equivalentes a las fn_generar_* SQL) ---
        v_antecedentes = fn_generar_antecedentes(v_es_zero)

        if p_uci:
            v_sintomas = fn_generar_sintomas(True)
            v_signos = fn_generar_signos_vitales(True, 'critico')
        elif v_tipo_nota == 'Urgencia':
            v_sintomas = fn_generar_sintomas(v_es_zero)
            v_signos = fn_generar_signos_vitales(v_es_zero, 'urgencia')
        else:
            v_sintomas = fn_generar_sintomas(v_es_zero)
            v_signos = fn_generar_signos_vitales(v_es_zero, 'general')

        v_interrogatorio = fn_generar_interrogatorio(v_es_zero, v_genero, v_edad)
        v_auditoria = fn_generar_auditoria(p_usuario_ip)

        # --- Construir documento MongoDB ---
        documento = {
            "FechaRegistro": v_fecha_reg,
            "Estatus": 1,
            "TipoNota": v_tipo_nota,
            "AntecedentesRelevantes": v_antecedentes,
            "SintomasActuales": v_sintomas,
            "InterrogatorioAnamnesis": v_interrogatorio,
            "SignosVitales": v_signos,
            "Auditoria": v_auditoria,
            "Paciente_ID": v_paciente_id,
            "Medico_ID": v_medico_id,
            "Expediente_ID": v_expediente_id,
            "metadata_generacion": {
                "pediatria": p_pediatria,
                "uci": p_uci,
                "paciente_zero": v_es_zero,
                "edad_generada": v_edad,
                "genero_generado": v_genero
            }
        }

        notas_batch.append(documento)

        # Insertar en bloques de batch_size o al final
        if len(notas_batch) == batch_size or i == (p_cantidad - 1):
            coleccion.insert_many(notas_batch)
            insertados += len(notas_batch)
            notas_batch = []

    # --- Bitácora (equivalente al INSERT INTO tbi_bitacora del SQL) ---
    descripcion_log = (
        f"Configuración API: {p_cantidad} registros generados. "
        f"Tipos: [{', '.join(p_tipos_nota)}]. "
        f"Pediatria/UCI/Zero: {p_pediatria}/{p_uci}/{p_zero}"
    )
    log_bitacora_mongo("NotasMedicas", p_usuario_ip, "INSERT Pydantic", descripcion_log)

    return {
        "mensaje": f"¡Éxito! Tu IP ({p_usuario_ip}) inyectó un total de {insertados} registros médicos (NoSQL).",
        "parametros_usados": {
            "cantidad": p_cantidad,
            "tipos_nota": p_tipos_nota,
            "incluir_pediatria": p_pediatria,
            "incluir_uci": p_uci,
            "incluir_paciente_zero": p_zero
        },
        "registros_creados": insertados
    }
