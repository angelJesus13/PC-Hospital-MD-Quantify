"""
Equivalente Python de fn_generar_signos_vitales.sql para MongoDB.
Genera signos vitales según escenario clínico.
En MongoDB retorna un DICT (subdocumento anidado) en vez del string ENUM de SQL.
"""
import random


def fn_generar_signos_vitales(p_es_paciente_zero: bool, p_escenario: str = "general") -> dict:
    """
    Replica de la función SQL fn_generar_signos_vitales, 
    adaptada para MongoDB retornando un subdocumento con campos individuales.
    
    Args:
        p_es_paciente_zero: Si el paciente es desconocido/zero.
        p_escenario: Escenario clínico ('general', 'urgencia', 'uci', 'critico').
        
    Returns:
        Dict con signos vitales como subdocumento para MongoDB.
    """
    if p_es_paciente_zero:
        return {
            "presion_arterial": "No recabados",
            "frecuencia_cardiaca": 0,
            "frecuencia_respiratoria": 0,
            "temperatura_c": 0.0,
            "saturacion_o2": 0,
            "recabados": False
        }

    p_escenario = p_escenario.lower()

    if p_escenario in ('uci', 'critico'):
        # Crítico — Replica exacta del SQL: FC:130, FR:28, TA:160/100, Temp:39.0, SpO2:88%
        return {
            "presion_arterial": "160/100",
            "frecuencia_cardiaca": 130,
            "frecuencia_respiratoria": 28,
            "temperatura_c": 39.0,
            "saturacion_o2": 88,
            "recabados": True,
            "nivel_gravedad": "Crítico"
        }
    elif p_escenario == 'urgencia':
        # Alterado — Replica exacta del SQL: FC:110, FR:24, TA:140/90, Temp:38.5, SpO2:92%
        return {
            "presion_arterial": "140/90",
            "frecuencia_cardiaca": 110,
            "frecuencia_respiratoria": 24,
            "temperatura_c": 38.5,
            "saturacion_o2": 92,
            "recabados": True,
            "nivel_gravedad": "Alterado"
        }
    else:
        # General — Distribución ponderada idéntica al SQL
        v_rand = random.random()
        if v_rand < 0.5:
            # FC:80, FR:16, TA:120/80, Temp:36.5, SpO2:98%
            return {
                "presion_arterial": "120/80",
                "frecuencia_cardiaca": 80,
                "frecuencia_respiratoria": 16,
                "temperatura_c": 36.5,
                "saturacion_o2": 98,
                "recabados": True,
                "nivel_gravedad": "Normal"
            }
        elif v_rand < 0.8:
            # FC:95, FR:20, TA:130/85, Temp:37.2, SpO2:96%
            return {
                "presion_arterial": "130/85",
                "frecuencia_cardiaca": 95,
                "frecuencia_respiratoria": 20,
                "temperatura_c": 37.2,
                "saturacion_o2": 96,
                "recabados": True,
                "nivel_gravedad": "Leve"
            }
        else:
            # FC:60, FR:14, TA:100/60, Temp:36.0, SpO2:95%
            return {
                "presion_arterial": "100/60",
                "frecuencia_cardiaca": 60,
                "frecuencia_respiratoria": 14,
                "temperatura_c": 36.0,
                "saturacion_o2": 95,
                "recabados": True,
                "nivel_gravedad": "Normal"
            }
