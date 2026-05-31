"""
Equivalente Python de fn_generar_auditoria.sql para MongoDB.
Genera estatus de auditoría clínica MECIC y NOM-004-SSA3-2012.
Retorna un dict con campos de auditoría (subdocumento para MongoDB).
"""
import random
import string
from datetime import datetime, timedelta


def fn_generar_auditoria(p_usuario_ip: str = "") -> dict:
    """
    Replica exacta de la función SQL fn_generar_auditoria, 
    extendida con la lógica de generar_bloque_auditoria() de clinical_simulator.py
    para aprovechar la flexibilidad de subdocumentos en MongoDB.
    
    Args:
        p_usuario_ip: IP del usuario (mantenido para compatibilidad de firma).
        
    Returns:
        Dict con campos de auditoría para insertar como subdocumento en MongoDB.
    """
    v_rand = random.random()

    # Distribución idéntica al SQL:
    # < 0.50 → Pendiente
    # < 0.70 → Aprobado
    # < 0.85 → Observación Menor
    # < 0.95 → Observación Mayor
    # < 0.98 → No Cumple
    # >= 0.98 → Crítico

    if v_rand < 0.50:
        estatus = "Pendiente de Auditoría Clínica MECIC"
    elif v_rand < 0.70:
        estatus = "Aprobado: Cumple con todos los dominios normativos de la NOM-004-SSA3-2012"
    elif v_rand < 0.85:
        estatus = "Observación Menor: Exploración física no describe detalladamente patrón céfalo-caudal"
    elif v_rand < 0.95:
        estatus = "Observación Mayor: Falta justificación clínica detallada para el pronóstico y tratamiento"
    elif v_rand < 0.98:
        estatus = "No Cumple (NOM-004): Notas clínicas incompletas o falta de congruencia diagnóstico-terapéutica"
    else:
        estatus = "Crítico: Riesgo médico-legal, documentación insuficiente del acto médico"

    # Subdocumento enriquecido para MongoDB (aprovechando flexibilidad NoSQL)
    fecha_base = datetime.utcnow() - timedelta(days=random.randint(0, 365))

    auditoria = {
        "firma_digital_medico": ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
        "fecha_emision": fecha_base,
        "estatus_auditoria": estatus
    }

    # ~35% de las notas caen en revisión de auditoría (ya auditadas)
    es_auditada = random.random() < 0.35
    if es_auditada:
        auditoria["fecha_auditoria"] = fecha_base + timedelta(hours=random.randint(12, 120))
        auditoria["auditor_medico_id"] = f"AUDITOR-{random.randint(100, 999)}"

        if "No Cumple" in estatus or "Crítico" in estatus or "Observación Mayor" in estatus:
            auditoria["calificacion_calidad_100"] = random.randint(30, 69)
            auditoria["hallazgos_criticos"] = random.choice([
                "Omitió antecedentes médicos cruzados del paciente.",
                "Incongruencia farma-diagnóstico detectable en el SOAP.",
                "Falta de folio del dictador transcrito adjunto.",
                "Ausencia de signos vitales para egreso forzoso.",
                "Excedió el tiempo de respuesta normativo en urgencias."
            ])
        else:
            auditoria["calificacion_calidad_100"] = random.randint(70, 100)

    return auditoria
