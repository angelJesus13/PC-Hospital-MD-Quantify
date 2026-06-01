# Requerimientos Funcionales (FRs) - PC-Hospital-MD

Este documento define de forma específica las operaciones funcionales que el sistema de registros médicos (desarrollado con React, Express, Node y bases de datos híbridas) debe ejecutar.

## 1. Módulo de Autenticación y Perfiles (MySQL)
*   **FR-01:** La API debe permitir el inicio de sesión de roles administrativos y profesionales de salud, validando contraseñas cifradas (bcrypt) y retornando un token JWT.
*   **FR-02:** El sistema administrativo debe permitir el registro (CRUD) de expedientes de pacientes y la creación de perfiles para los médicos.
*   **FR-03:** El sistema debe restringir el acceso a los datos de salud únicamente a los profesionales que estén directamente asignados al paciente correspondiente en la tabla `paciente_profesional`.

## 2. Ingesta de Datos Médicos (MongoDB)
*   **FR-04:** La API debe proporcionar un endpoint asíncrono para recibir peticiones estructuradas con métricas vitales (ritmo cardíaco, oxígeno, pasos) provenientes de dispositivos wearables vinculados a los pacientes.
*   **FR-05:** Todo registro biométrico debe almacenarse de manera persistente en la colección `wearable_logs` de MongoDB, asociando la marca de tiempo exacta (`capturedAt`) y el `patientId`.

## 3. Motor de Reglas y Alertas Clínicas
*   **FR-06:** El sistema de backend debe evaluar los signos vitales entrantes contra umbrales médicos estándar (ej. detectar taquicardias).
*   **FR-07:** Si se detecta un valor riesgoso, la API debe generar automáticamente un registro en la tabla de `alertas` (MySQL) e incluir la severidad y el tipo de alerta.
*   **FR-08:** Las notificaciones de alerta deben ser enviadas en tiempo real (vía Socket.IO) al dashboard del médico responsable.

## 4. Consultas de Historial Médico
*   **FR-09:** Los médicos deben poder consultar desde su panel una gráfica consolidada del historial biométrico de los pacientes filtrada por fecha.
