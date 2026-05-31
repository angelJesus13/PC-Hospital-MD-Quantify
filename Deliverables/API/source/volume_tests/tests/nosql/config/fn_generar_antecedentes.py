"""
Equivalente Python de fn_generar_antecedentes.sql para MongoDB.
Genera antecedentes clínicos aleatorios: crónicos, alergias, cirugías previas.
Retorna None si paciente_zero o si cae en el 40% sin antecedentes.
"""
import random


def fn_generar_antecedentes(p_es_paciente_zero: bool) -> str | None:
    """
    Replica exacta de la función SQL fn_generar_antecedentes.
    
    Args:
        p_es_paciente_zero: Si el paciente es desconocido/zero.
        
    Returns:
        String con antecedentes concatenados, o None.
    """
    if p_es_paciente_zero:
        return None

    # 40% pacientes sin antecedentes relevantes reportados al ingresar nota
    if random.random() < 0.40:
        return None

    cronicas = [
        'Sin comorbilidades',
        'Hipertensión Arterial Sistémica (HAS) controlada',
        'Diabetes Mellitus Tipo 2 (DM2) en manejo',
        'HAS + DM2 de 10 años de diagnóstico',
        'Hipotiroidismo',
        'Asma bronquial intermitente',
        'Tabaquismo intenso (IT>20)',
        'Alcoholismo social'
    ]

    alergias = [
        'Sin alergias medicamentosas',
        'Alérgico a Penicilina',
        'Alérgico a AINEs',
        'Alérgico a Sulfamidas',
        'Alergia alimentaria (Mariscos)'
    ]

    cirugias = [
        'Sin cirugías previas',
        'Colecistectomía',
        'Apendicectomía',
        'Cesárea',
        'Amigdalectomía'
    ]

    v_cronica = random.choice(cronicas)
    v_alergias = random.choice(alergias)
    v_cx = random.choice(cirugias)

    return f"Crónicos: {v_cronica} | Alergias: {v_alergias} | Cx previas: {v_cx}"
