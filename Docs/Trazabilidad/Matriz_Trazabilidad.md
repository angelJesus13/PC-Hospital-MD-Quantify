# Matriz de Trazabilidad Completa - PC-Hospital-MD

Para garantizar la calidad de la documentación (cumpliendo con metodologías de Ingeniería de Software Rigurosa), esta matriz evidencia la correspondencia bidireccional entre los Requerimientos de Negocio, Funcionales, No Funcionales, Historias de Usuario y Casos de Prueba.

| Ref. Negocio (BR) | Ref. Funcional (FR) | Historia de Usuario (UH) | Ref. Usuario (UR) | Atributo de Calidad (NFR) | Caso de Prueba (QA) | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BR-03** (Viabilidad) | **FR-01** (Login y Accesos) | **UH-01** (Autenticación del Personal) | **UR-03** (Admin) | **NFR-03, NFR-04** (Bcrypt, JWT) | **Test 1** (Aislamiento MySQL) | Validado |
| **BR-01** (Monitoreo) | **FR-02** (Ingesta Biométrica) | **UH-02** (Ingesta ininterrumpida) | **UR-02** (Paciente) | **NFR-01** (MongoDB Stress) | **Test 2** (300k Registros) | Validado |
| **BR-01** (Monitoreo) | **FR-09** (Consultas Historial) | **UH-03** (Gráfica de Salud) | **UR-01** (Médico) | **NFR-02** (250ms Response) | **Test 4** (Consulta EHR) | Validado |
| **BR-02** (Alertas) | **FR-03** (Alertas Clínicas) | **UH-04** (Notificación de Riesgo) | **UR-01** (Médico) | **NFR-05** (Socket.IO Latency) | **Test 3** (Disparo de Alertas) | Validado |

## Criterio Evaluativo
Cada requerimiento en la aplicación (`BR -> FR -> UH -> Esquema -> Pruebas`) posee trazabilidad explícita, asegurando que si cambia una regla de negocio de Alertas Médicas (BR-02), los equipos de desarrollo sabrán exactamente qué endpoint (FR-03), historia (UH-04) y caso de prueba (Test 3) se verán afectados.
