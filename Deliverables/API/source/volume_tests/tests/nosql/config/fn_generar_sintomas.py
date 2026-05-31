"""
Equivalente Python de fn_generar_sintomas.sql para MongoDB.
Genera síntomas clínicos aleatorios con intensidad EVA y evolución temporal.
Retorna texto especial de trauma severo para paciente_zero.
"""
import random


def fn_generar_sintomas(p_es_paciente_zero: bool) -> str:
    """
    Replica exacta de la función SQL fn_generar_sintomas.
    
    Args:
        p_es_paciente_zero: Si el paciente es desconocido/zero.
        
    Returns:
        String con síntomas, intensidad EVA y evolución temporal.
    """
    if p_es_paciente_zero:
        return (
            "Paciente ingresa en calidad de desconocido. Inconsciente (Escala de Glasgow < 8). "
            "Se observan múltiples contusiones y signos de trauma severo. "
            "No responde a estímulos verbales ni dolorosos."
        )

    # 15 variantes de síntomas (idénticas al SQL)
    sintomas = [
        'Dolor torácico opresivo irradiado a brazo izquierdo',
        'Disnea de esfuerzo y sensación de ahogo',
        'Cefalea intensa de inicio súbito, pulsátil',
        'Fiebre no cuantificada, escalofríos y diaforesis',
        'Dolor abdominal difuso con rebote y resistencia',
        'Náusea persistente y episodios eméticos de contenido biliar',
        'Debilidad generalizada, astenia y adinamia',
        'Confusión aguda y desorientación',
        'Palpitaciones rápidas e irregulares',
        'Dificultad para movilizar hemicuerpo derecho',
        'Dolor lumbar irradiado a extremidad inferior derecha',
        'Poliuria, polidipsia y visión borrosa',
        'Tos productiva con expectoración verdosa',
        'Sibilancias audibles a distancia y tiraje intercostal',
        'Sangrado transvaginal moderado con coágulos'
    ]

    # Evolución temporal (8 variantes, idénticas al SQL)
    tiempos = [
        '3 horas', '12 horas', '24 horas', '2 días',
        '4 días', '1 semana', '2 semanas', '1 mes'
    ]

    v_sintoma = random.choice(sintomas)
    v_intensidad = random.randint(1, 10)
    v_tiempo = random.choice(tiempos)

    return f"{v_sintoma} | EVA {v_intensidad}/10 | Evolución de {v_tiempo}"
