"""
Equivalente Python de fn_generar_tipo_nota.sql para MongoDB.
Genera tipo de nota médica con distribución ponderada idéntica al SQL.
"""
import random


def fn_generar_tipo_nota() -> str:
    """
    Replica exacta de la función SQL fn_generar_tipo_nota.
    Distribución ponderada:
        < 0.10 → Ingreso      (10%)
        < 0.45 → Evolución    (35%)
        < 0.65 → Urgencia     (20%)
        < 0.80 → Interconsulta (15%)
        >= 0.80 → Egreso      (20%)
    
    Returns:
        String con el tipo de nota médica.
    """
    v_rand = random.random()

    if v_rand < 0.10:
        return 'Ingreso'
    elif v_rand < 0.45:
        return 'Evolución'
    elif v_rand < 0.65:
        return 'Urgencia'
    elif v_rand < 0.80:
        return 'Interconsulta'
    else:
        return 'Egreso'
