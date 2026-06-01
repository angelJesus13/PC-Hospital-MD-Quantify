# Historias de Usuario (UHs) - PC-Hospital-MD

Estas historias de usuario detallan los flujos desde la perspectiva ágil para construir los microservicios y vistas del expediente clínico y el monitoreo biométrico.

## Épica 1: Expediente Clínico y Asignaciones (SQL)
*   **UH-01: Alta de Paciente.** *Como* administrador del sistema, *quiero* rellenar un formulario con los datos demográficos y de contacto de un nuevo paciente, *para* crear su perfil maestro en la tabla de `pacientes` (MySQL).
*   **UH-02: Asignación Profesional.** *Como* administrador, *quiero* relacionar la identificación de un profesional de la salud con la identificación de un paciente, *para* garantizar que el médico pueda visualizar los datos médicos correspondientes (Tabla puente `paciente_profesional`).

## Épica 2: Captura Biométrica y Visibilidad (NoSQL / Frontend)
*   **UH-03: Ingesta Ininterrumpida.** *Como* API de Backend, *quiero* aceptar llamadas POST masivas desde dispositivos Wearable, *para* almacenar el ritmo cardíaco y niveles de oxígeno en MongoDB de manera escalable.
*   **UH-04: Gráfica de Tendencias.** *Como* médico tratante, *quiero* abrir el expediente de mi paciente y ver un componente interactivo de gráficas (React), *para* analizar visualmente sus signos vitales de los últimos días.

## Épica 3: Autenticación y Alertas (Seguridad / WebSockets)
*   **UH-05: Login Autorizado.** *Como* usuario administrativo o médico, *quiero* iniciar sesión, *para* obtener un Token que me permita navegar por el Dashboard.
*   **UH-06: Notificación Crítica.** *Como* motor de validación interno, *quiero* evaluar cada métrica biométrica recibida; si cruza el umbral clínico configurado, *quiero* insertar un registro en la tabla de `alertas` y disparar un socket, *para* avisar a la interfaz del médico.
