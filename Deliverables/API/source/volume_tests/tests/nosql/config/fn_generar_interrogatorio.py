"""
Equivalente Python de fn_generar_interrogatorio.sql para MongoDB.
Genera texto de interrogatorio clínico (anamnesis) usando género, edad y tiempo de evolución.
Retorna texto especial para paciente_zero.
"""
import random


def fn_generar_interrogatorio(p_es_paciente_zero: bool, p_genero: str = None, p_edad: int = None) -> str:
    """
    Replica exacta de la función SQL fn_generar_interrogatorio.
    
    Args:
        p_es_paciente_zero: Si el paciente es desconocido/zero.
        p_genero: Género del paciente ('hombre' o 'mujer').
        p_edad: Edad del paciente en años.
        
    Returns:
        String con el texto del interrogatorio clínico.
    """
    if p_es_paciente_zero:
        return (
            "PACIENTE ZERO. Ingresa en calidad de desconocido. "
            "No es posible recabar interrogatorio directo por estado de inconsciencia "
            "ni indirecto por ausencia de familiares. Abordaje emergente."
        )

    tiempos = [
        'pocas horas',
        'esta misma mañana',
        'la noche anterior',
        'hace 3 días',
        'hace una semana',
        'de forma gradual'
    ]

    estados = [
        'Paciente acude consciente y orientado en sus 3 esferas.',
        'Acude con facies de dolor intenso y marcha claudicante.',
        'Se observa hemodinámicamente estable pero refiriendo molestia persistente.',
        'Ingresa acompañado de familiar refiriendo deterioro del estado general.',
        'Acude ansioso/a solicitando atención médica inmediata en triaje.'
    ]

    v_tiempo = random.choice(tiempos)
    v_estado = random.choice(estados)

    genero_texto = (p_genero or 'de género no especificado').lower()
    edad_texto = p_edad if p_edad is not None else 0

    return (
        f"Paciente {genero_texto} de {edad_texto} años. "
        f"Inicia su padecimiento actual {v_tiempo}. {v_estado}"
    )
