# Manual de Pruebas - PC-Hospital-MD

Este manual describe los procedimientos de control de calidad (QA) y pruebas de integración cruciales para un sistema enfocado en la salud y el monitoreo de pacientes.

## Casos de Prueba Críticos (EHR y Monitoreo)

### Test 1: Seguridad y Aislamiento de Datos
*   **Precondición:** Médico A tiene asignado al Paciente 1. Médico B tiene asignado al Paciente 2.
*   **Ejecución:** El Médico A intenta acceder mediante la WebApp o un cliente REST al expediente del Paciente 2 usando su ID de historia clínica.
*   **Criterio de Éxito:** La API deniega el acceso con `403 Forbidden`, confirmando que el motor SQL verifica correctamente la relación en la tabla `paciente_profesional` antes de devolver cualquier registro biométrico de MongoDB.

### Test 2: Sobrecarga de Base de Datos NoSQL
*   **Precondición:** El servidor está en ambiente de simulación.
*   **Ejecución:** Mediante herramientas de estrés de API (ej. Artillery), enviar 300,000 peticiones de simulación biométrica a `/api/wearables/ingest` durante 10 minutos.
*   **Criterio de Éxito:** La base de datos documental (MongoDB) logra absorber la escritura masiva. En paralelo, un administrador intenta dar de alta a un médico nuevo en MySQL sin experimentar latencias, demostrando la eficacia de la Arquitectura Híbrida.

### Test 3: Fiabilidad de las Alertas en Tiempo Real
*   **Precondición:** Paciente bajo monitoreo con dispositivo emparejado y médico con sesión activa en el Dashboard.
*   **Ejecución:** Se induce desde el dispositivo WearableApp una señal crítica (ej. caída extrema de oxígeno).
*   **Criterio de Éxito:** La alerta sonora o visual (Socket.IO) aparece en la pantalla del médico en menos de 1 segundo tras la inyección del dato. La alerta debe quedar permanentemente registrada en el historial de eventos del paciente.
