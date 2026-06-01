# Requerimientos Funcionales (FRs) - PC-Hospital-MD

Este documento define las operaciones funcionales del ecosistema hospitalario, detallando entradas, salidas, precondiciones, flujos alternativos y criterios de aceptación, con trazabilidad directa a Historias de Usuario (UHs).

## Módulo 1: Autenticación y Control de Accesos
### FR-01: Autenticación de Personal Médico
*   **Descripción:** El sistema debe permitir el inicio de sesión de roles administrativos y profesionales de salud.
*   **Entradas:** `email` (string), `password` (string).
*   **Salidas:** JWT Token (string), `userId` (UUID), `role` (string).
*   **Precondiciones:** El usuario debe existir en la base de datos MySQL con estado "Activo".
*   **Flujo Principal:** El usuario ingresa credenciales válidas -> El sistema cifra la contraseña y valida contra BBDD -> Retorna HTTP 200 y el token JWT.
*   **Flujo Alternativo (Error):** Si las credenciales son inválidas -> El sistema retorna HTTP 401 "Unauthorized" sin generar token.
*   **Criterio de Aceptación:** El inicio de sesión debe completarse en menos de 500ms y el token JWT debe estar firmado con RS256.
*   **Trazabilidad:** Asociado a UH-05.

## Módulo 2: Ingesta Biométrica (NoSQL)
### FR-02: Recepción de Datos desde Wearables
*   **Descripción:** La API REST proporcionará un endpoint asíncrono para recibir métricas continuas desde dispositivos de pacientes.
*   **Entradas:** Payload JSON conteniendo `patientId`, `deviceId`, `heartRate`, `spO2`, `steps`.
*   **Salidas:** Código HTTP 201 Created.
*   **Precondiciones:** El `deviceId` debe estar vinculado a un `patientId` activo en la base de datos MySQL.
*   **Flujo Principal:** Wearable envía payload POST -> La API recibe, asigna un `capturedAt` y guarda el documento en la colección `wearable_logs` de MongoDB -> Responde 201.
*   **Flujo Alternativo:** Si el payload está incompleto (ej. falta `patientId`) -> La API retorna HTTP 400 "Bad Request".
*   **Criterio de Aceptación:** El sistema debe soportar ráfagas asíncronas, garantizando inserción sin bloqueos (non-blocking I/O).
*   **Trazabilidad:** Asociado a UH-03.

## Módulo 3: Motor de Alertas Clínicas
### FR-03: Generación de Alertas por Anomalías Vitales
*   **Descripción:** El backend evaluará en tiempo real si las métricas biométricas superan los umbrales seguros.
*   **Entradas:** Payload biométrico interno en memoria (ej. `heartRate > 100`).
*   **Salidas:** Registro SQL en tabla `alertas`, Evento `Socket.IO`.
*   **Precondiciones:** El servicio de evaluación (Motor de Alertas) debe estar activo tras la ingesta de datos.
*   **Flujo Principal:** Ingesta detecta anomalía -> Escribe alerta en MySQL vinculando `patientId` -> Emite evento push al front-end médico.
*   **Flujo Alternativo:** Falla en la conexión MySQL al escribir alerta -> El sistema encola el mensaje en RabbitMQ o similar para reintento automático.
*   **Criterio de Aceptación:** La latencia entre la detección y la notificación frontend no debe exceder 1 segundo.
*   **Trazabilidad:** Asociado a UH-06.
