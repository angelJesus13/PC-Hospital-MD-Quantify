# Evaluación de API - PC-Hospital-MD

Este documento concentra las métricas de calidad y pruebas de integración para la API de backend, construida sobre Node.js y Express.js, que interconecta el sistema hospitalario y los sensores biométricos.

## Criterios de Evaluación

### 1. Funcionalidad y Seguridad (JWT)
*   **Endpoint:** `POST /api/auth/login`
*   **Prueba:** Se envían credenciales de un médico. El sistema debe validar contra MySQL y retornar un código `200 OK` con el token JWT. Accesos con contraseña errónea deben ser bloqueados con `401 Unauthorized` sin dar pistas de la existencia del correo.

### 2. Ingesta Asíncrona (Wearables)
*   **Endpoint:** `POST /api/wearables/ingest`
*   **Prueba:** La simulación de hardware envía lecturas continuas. El endpoint debe guardar el documento JSON en MongoDB y retornar `201 Created` casi de manera instantánea para no agotar la batería ni el buffer del wearable.

### 3. Interceptor de Alertas Médicas
*   **Lógica Interna:** Se evalúa si el envío del payload del punto anterior activa el disparador (trigger) configurado en el backend.
*   **Prueba:** Si `heartRate > 100`, el sistema debe efectuar la escritura en la tabla MySQL de alertas médicas y responder por WebSockets, asegurando que el médico de guardia fue notificado.

## Ejecución
Las colecciones completas para Postman/Thunder Client se localizan en la raíz del entorno backend. Se recomienda auditar los tiempos de respuesta (idealmente < 200ms) al realizar consultas históricas masivas al perfil del paciente.
