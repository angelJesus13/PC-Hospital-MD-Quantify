# Historias de Usuario (UHs) - PC-Hospital-MD

Todas las historias están priorizadas bajo la técnica **MoSCoW** (Must, Should, Could, Won't have) y formuladas mediante criterios **Given-When-Then** (BDD).

## Épica 1: Expediente Clínico y Accesos
### UH-01: Autenticación del Personal
*   **Rol:** Médico / Administrador.
*   **Acción:** Iniciar sesión en el portal WebApp.
*   **Valor de Negocio:** Garantizar que los expedientes médicos estén protegidos contra accesos no autorizados, cumpliendo las normativas de salud.
*   **Priorización (MoSCoW):** **MUST HAVE** (Esencial para operar).
*   **Trazabilidad:** Asociado a **FR-01**.
*   **Criterio de Aceptación (BDD):**
    *   `Given` (Dado que) el médico ingresa su correo y contraseña correcta en el formulario de login.
    *   `When` (Cuando) presiona el botón "Entrar".
    *   `Then` (Entonces) el sistema autentica contra MySQL, devuelve un token JWT válido y redirige al Dashboard.

## Épica 2: Monitoreo Biométrico
### UH-02: Ingesta Ininterrumpida de Datos
*   **Rol:** Wearable (Sistema Cliente).
*   **Acción:** Enviar payload biométrico masivo a la API.
*   **Valor de Negocio:** Habilitar el monitoreo preventivo de pacientes ambulatorios para tomar decisiones clínicas basadas en datos recientes.
*   **Priorización (MoSCoW):** **MUST HAVE**.
*   **Trazabilidad:** Asociado a **FR-02**.
*   **Criterio de Aceptación (BDD):**
    *   `Given` que el dispositivo wearable del paciente está conectado a internet.
    *   `When` envía un payload válido con ritmo cardíaco al endpoint `/ingest`.
    *   `Then` la API recibe la información de forma asíncrona, la inserta en MongoDB sin demoras y devuelve HTTP 201.

### UH-03: Visualización de Gráficas de Salud
*   **Rol:** Médico.
*   **Acción:** Ver gráfica histórica de signos vitales.
*   **Valor de Negocio:** Permitir identificar visualmente tendencias degenerativas en la salud del paciente.
*   **Priorización (MoSCoW):** **SHOULD HAVE** (Alto impacto, pero no bloquea el sistema central).
*   **Trazabilidad:** Asociado a FR-09.
*   **Criterio de Aceptación (BDD):**
    *   `Given` que el médico se encuentra en la vista detallada del paciente en la WebApp.
    *   `When` selecciona el filtro "Últimos 7 días".
    *   `Then` el frontend renderiza un gráfico de líneas conectando los datos obtenidos desde la colección NoSQL del paciente.

## Épica 3: Sistema de Alertas Críticas
### UH-04: Notificación de Riesgo
*   **Rol:** Motor de Reglas (Backend).
*   **Acción:** Disparar notificación si el paciente sufre una anomalía.
*   **Valor de Negocio:** Reducir tiempos de reacción médica en caso de emergencias ambulatorias.
*   **Priorización (MoSCoW):** **MUST HAVE**.
*   **Trazabilidad:** Asociado a **FR-03**.
*   **Criterio de Aceptación (BDD):**
    *   `Given` que la API procesa un valor de `heartRate` > 100 lpm en estado de reposo.
    *   `When` ejecuta el algoritmo de validación de umbral.
    *   `Then` escribe inmediatamente el evento en la tabla SQL de alertas y envía un socket al dashboard del médico asignado.
