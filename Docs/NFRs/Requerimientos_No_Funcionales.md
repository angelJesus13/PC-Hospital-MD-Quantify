# Requerimientos No Funcionales (NFRs) - PC-Hospital-MD

Este documento establece las normativas de arquitectura híbrida, rendimiento y seguridad técnica, garantizando que el ecosistema clínico soporte operaciones críticas.

## 1. Arquitectura Híbrida
*   **NFR-01:** La arquitectura debe separar estrictamente los datos operativos (MySQL para pacientes y roles) de la analítica masiva (MongoDB para `wearable_logs`), asegurando que las tablas relacionales no se bloqueen por la alta frecuencia de escritura de biosensores.

## 2. Rendimiento
*   **NFR-02:** El procesamiento de la ingesta de wearables y su respectiva inserción en MongoDB no debe tomar más de **300 milisegundos**, operando mediante la asincronía de Node.js.
*   **NFR-03:** Las notificaciones enviadas a los tableros web de los médicos deben distribuirse con latencia mínima a través de WebSockets (Socket.IO).

## 3. Seguridad Médica y Privacidad
*   **NFR-04:** La base de datos relacional debe encriptar las contraseñas del personal médico. Todos los endpoints que consuman datos del paciente requieren autorización mediante un token (JWT).
*   **NFR-05:** Se deben realizar copias de seguridad de los expedientes mediante rutinas especializadas (ej. el script `backup_manager.py` ubicado en `DataBases/SQL`).

## 4. Despliegue y Pruebas
*   **NFR-06:** La API debe pasar favorablemente la evaluación del documento `API_Quality_Evaluation.md`, comprobando un control robusto contra inyecciones de dependencias y caídas por excepciones no capturadas.
