"""
Motor Clínico Maestro para MongoDB.
Refactorizado para importar desde los módulos de tests/nosql/config/
que replican la funcionalidad de las funciones SQL.

Mantiene la interfaz original (compilar_caso_clinico_maestro) usada por notas.py.
"""
import random
from datetime import datetime

from tests.nosql.config.fn_generar_antecedentes import fn_generar_antecedentes
from tests.nosql.config.fn_generar_auditoria import fn_generar_auditoria
from tests.nosql.config.fn_generar_interrogatorio import fn_generar_interrogatorio
from tests.nosql.config.fn_generar_signos_vitales import fn_generar_signos_vitales
from tests.nosql.config.fn_generar_sintomas import fn_generar_sintomas
from tests.nosql.config.fn_generar_tipo_nota import fn_generar_tipo_nota


# -------------------------------------------------------------
# MATRICES CLÍNICAS BASE (Usadas por el orquestador para
# enriquecer los documentos NoSQL con contexto patológico)
# -------------------------------------------------------------
MATRICES_BASES = [
    {
        "etiqueta": "Trauma",
        "motivos": [
            "Choque frontal",
            "Precipitación de 3 metros de altura",
            "Herida por arma de fuego en extremidad",
            "Síndrome de aplastamiento"
        ],
        "sintoma": "Paciente ingresa en camilla rígida refiriendo dolor incontrolable y hemorragia activa.",
        "es_zero_probable": True
    },
    {
        "etiqueta": "Paro",
        "motivos": [
            "Paro Cardiorrespiratorio Cód. Azul",
            "Muerte en Arribo a Triage",
            "Fibrilación Ventricular Idiopática"
        ],
        "sintoma": "Ingresado sin respuesta motora ni verbal. Inicio de RCP de ciclo urgente.",
        "es_zero_probable": True
    },
    {
        "etiqueta": "Hipertensiva",
        "motivos": [
            "Crisis Hipertensiva de Emergencia",
            "Encefalopatía Hipertensiva"
        ],
        "sintoma": "Describe cefalea universal occipital punzante de 10/10, vértigo crónico, rubicundez.",
        "es_zero_probable": False
    },
    {
        "etiqueta": "Infeccioso",
        "motivos": [
            "Sepsis Oculta Confirmada",
            "Shock Séptico Foco Abdominal",
            "Faringoamigdalitis Supurativa Larga"
        ],
        "sintoma": "Diaforesis profusa, tos de 5 días de evolución, mialgias con astenia y expectoración purulenta.",
        "es_zero_probable": False
    },
    {
        "etiqueta": "Pediátrica",
        "motivos": [
            "Egreso de Recién Nacido Término Sano",
            "Revisión Pediátrica Mensual Programada"
        ],
        "sintoma": "Neonato alerta, reactivo al entorno. Alojamiento transitorio correcto, nutrición de ceno conservada.",
        "es_zero_probable": False
    },
    {
        "etiqueta": "Estable",
        "motivos": [
            "Dolor Abdominal no Específico Referido",
            "Gastritis Erosiva Intermitente",
            "Cefalea Tensional Laboral"
        ],
        "sintoma": "Paciente deambula, cooperador. Refiere dolor agudo pero leve que cede parcialmente con ingesta de IBP.",
        "es_zero_probable": False
    }
]

COMPLEMENTOS_SINTOMAS = [
    "Niega alergias comprobadas a Beta-lactámicos.",
    "Su esquema de vacunación es incierto.",
    "No aporta laboratorios de diagnóstico externo.",
    "Refiere ayuno mayor a 8 horas."
]


# -------------------------------------------------------------
# EXPLORACIÓN CEFALOCAUDAL (Procedimiento Anatómico)
# Mantiene la lógica rica del clinical_simulator original
# -------------------------------------------------------------
def sintetizar_exploracion(tipo: str) -> str:
    """Genera texto de exploración física cefalocaudal."""
    cabeza_cuello = [
        "Cráneo normocéfalo, sin endostosis ni exostosis. Pupilas isocóricas y normorreflécticas.",
        "Cráneo íntegro. Escleras limpias, mucosas nasales permeables.",
        "Pupilas anisocóricas de lento reflejo. Faringe hiperémica, no exudado.",
        "Cuello cilíndrico, tráquea central, pulso carotídeo rítmico. Ausencia de soplos carotídeos.",
        "Cuello móvil, doloroso a la palpación muscular, sin adenomegalias ni red venosa colateral."
    ]
    torax = [
        "Tórax normolíneo. Ruidos cardíacos rítmicos, buen tono e intensidad, sin soplos.",
        "Tórax en tonel, movimientos respiratorios disminuidos. Sibilancias basales.",
        "Campos pulmonares ventilados. Ventilación simétrica, claro pulmonar percutorio.",
        "Ruidos cardíacos arrítmicos, con soplo sistólico grado II/VI en foco aórtico.",
        "Hemitórax simétricos, sin uso de musculatura accesoria, murmullo vesicular presente."
    ]
    abdomen = [
        "Abdomen blando, depresible, no doloroso a la palpación, ruidos hidroaéreos audibles.",
        "Abdomen globoso, timpánico a la percusión, red venosa colateral ausente.",
        "Abdomen con defensa muscular involuntaria. Positivo a Murphy y McBurney. Peristalsis ausente.",
        "Cicatriz quirúrgica media apendicular. Abdomen depresible, rebote negativo.",
        "Hígado palpable a 2cm por debajo del reborde costal. Sin esplenomegalia palpable."
    ]
    extremidades = [
        "Extremidades superiores e inferiores íntegras, simétricas, tono y trofismo muscular conservado.",
        "Extremidades íntegras, pulsos pedios presentes y sincrónicos. Llenado capilar 2 segundos.",
        "Edema pretibial ++/++++ crónico bilateral. Fuerza muscular 4/5 generalizada.",
        "Extremidad derecha con luxación aparente, limitación de movimiento doloroso al tracto.",
        "Pulsos distales fuertes. Reflejos osteotendinosos 2/4. Sin signos autonómicos de alarma."
    ]

    exploracion_generada = "EXPLORACIÓN CEFALOCAUDAL: "
    exploracion_generada += random.choice(cabeza_cuello) + " "
    exploracion_generada += random.choice(torax) + " "
    exploracion_generada += random.choice(abdomen) + " "
    exploracion_generada += random.choice(extremidades)

    if "Trauma" in tipo:
        exploracion_generada = "Paciente inmovilizado con collarín cervical. " + exploracion_generada + " (NOTA: Glasgow inicial a documentar en hoja de Trauma)."
    elif "Paro" in tipo:
        exploracion_generada = "Paciente arréflexico. " + exploracion_generada + " Ausencia comprobada y persistente de pulso central y periférico."

    return exploracion_generada


# -------------------------------------------------------------
# ORQUESTADOR PRINCIPAL (Interfaz pública usada por notas.py)
# Ahora importa las funciones modulares de config/
# -------------------------------------------------------------
def compilar_caso_clinico_maestro(foco_clinico=None, ids_pacientes=None, ids_personal_medico=None, ids_expedientes=None):
    """
    Genera un documento completo de nota médica para MongoDB.
    Usa las funciones modulares de tests/nosql/config/ para generar cada campo,
    replicando la misma estructura que el SP de SQL pero aprovechando subdocumentos.
    """
    if foco_clinico:
        matrices_permitidas = [m for m in MATRICES_BASES if m["etiqueta"] in foco_clinico]
        if not matrices_permitidas:
            matrices_permitidas = MATRICES_BASES
    else:
        matrices_permitidas = MATRICES_BASES

    matriz_interna = random.choice(matrices_permitidas)
    
    # --- Tipo de nota usando la función modular ---
    tipo_escogido = fn_generar_tipo_nota()

    # --- Restricciones Lógicas (Business Rules) ---
    if matriz_interna["etiqueta"] == "Paro" and tipo_escogido == "Egreso":
        tipo_escogido = "Urgencia"
    if matriz_interna["etiqueta"] == "Pediátrica" and tipo_escogido == "Ingreso":
        tipo_escogido = "Egreso"

    # --- Llaves foráneas de MySQL ---
    fk_paciente = random.choice(ids_pacientes) if ids_pacientes else random.randint(1, 150)
    fk_personal_medico = random.choice(ids_personal_medico) if ids_personal_medico else random.randint(1, 50)
    fk_expediente = fk_paciente

    # --- Determinar si es paciente zero ---
    es_zero = matriz_interna.get("es_zero_probable", False) and random.random() < 0.15

    # --- Edad y género ---
    if matriz_interna["etiqueta"] == "Pediátrica":
        v_edad = random.randint(0, 14)
    else:
        v_edad = random.randint(18, 77)
    v_genero = 'hombre' if random.random() < 0.5 else 'mujer'

    # --- Determinar escenario clínico para signos vitales ---
    if matriz_interna["etiqueta"] in ("Paro",):
        escenario = "critico"
    elif matriz_interna["etiqueta"] in ("Trauma", "Hipertensiva"):
        escenario = "urgencia"
    else:
        escenario = "general"

    # --- Generar campos usando funciones modulares de config/ ---
    nota = {
        "FechaRegistro": datetime.utcnow(),
        "Estatus": 1,
        "TipoNota": tipo_escogido,
        "AntecedentesRelevantes": fn_generar_antecedentes(es_zero) or f"[{matriz_interna['etiqueta'].upper()}] - {random.choice(matriz_interna['motivos'])} detectado hace {random.randint(2, 60)} hrs.",
        "SintomasActuales": fn_generar_sintomas(es_zero) if es_zero else matriz_interna["sintoma"] + " " + random.choice(COMPLEMENTOS_SINTOMAS),
        "InterrogatorioAnamnesis": fn_generar_interrogatorio(es_zero, v_genero, v_edad),
        "ExploracionFisica": sintetizar_exploracion(matriz_interna['etiqueta']),
        "SignosVitales": fn_generar_signos_vitales(es_zero, escenario),
        "Auditoria": fn_generar_auditoria(),
        "Paciente_ID": fk_paciente,
        "Medico_ID": fk_personal_medico,
        "Expediente_ID": fk_expediente
    }

    return nota
