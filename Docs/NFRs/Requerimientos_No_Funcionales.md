# Requerimientos No Funcionales (NFRs) - PC-Hospital-MD

Este documento enuncia los atributos de calidad del sistema con métricas rigurosas y comprobables (SLAs, rendimiento y algoritmos de seguridad).

## 1. Arquitectura y Rendimiento (Performance)
*   **NFR-01 (Escalabilidad Híbrida):** La colección `wearable_logs` en MongoDB debe estar diseñada para soportar hasta **300,000 inserciones continuas** (stress testing) en ventanas de 10 minutos sin degradar los tiempos de la API.
*   **NFR-02 (Tiempos de Respuesta - SLAs):** Toda operación de sólo lectura (GET) sobre el expediente clínico (EHR) en MySQL debe resolver en un tiempo máximo de **250 milisegundos (p95)**. Las peticiones de escritura a MongoDB (POST /ingest) no deben exceder **150 milisegundos**.

## 2. Seguridad de la Información (Security)
*   **NFR-03 (Cifrado en Tránsito y Reposo):** Toda transmisión de datos biométricos entre el Wearable y la API debe ejecutarse sobre el protocolo **HTTPS mediante TLS 1.3**. Las contraseñas en MySQL deben estar hasheadas utilizando el algoritmo **Bcrypt con un factor de trabajo (salt rounds) de 10**.
*   **NFR-04 (Mecanismo de Autorización):** El acceso a la plataforma requiere autenticación basada en **JSON Web Tokens (JWT)**. Los tokens deben firmarse mediante un algoritmo asimétrico (**RS256**) y tener un periodo de expiración estricto de **2 horas (TTL)**, tras lo cual se exigirá un *refresh token*.
*   **NFR-05 (Cumplimiento de Privacidad):** El sistema debe enmascarar los datos personales identificables (PII) en los logs de depuración (API audit logs) para proteger la privacidad del paciente según normativas de salud.

## 3. Fiabilidad y Alta Disponibilidad (Reliability)
*   **NFR-06 (Uptime y Tolerancia a Fallos):** El entorno de producción deberá garantizar un acuerdo de nivel de servicio (SLA) de **99.9% de Uptime** mensual.
*   **NFR-07 (Procedimiento de Respaldo):** Se requiere la ejecución automatizada del script `backup_manager.py` cada 24 horas a las 03:00 AM (UTC) para realizar volcados (dumps) seguros de MySQL, con política de retención en almacenamiento en frío de 30 días.
