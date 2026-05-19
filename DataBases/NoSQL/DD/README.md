# DD - Diccionario de Datos NoSQL

## Descripcion general

Esta carpeta contiene el diccionario de datos para las colecciones NoSQL del proyecto **PC-Hospital-MD-Quantify**. Su proposito es explicar el significado de cada campo usado en documentos JSON o BSON.

## Diccionario general

| Campo | Coleccion | Tipo | Obligatorio | Descripcion |
| --- | --- | --- | --- | --- |
| `_id` | Todas | ObjectId | Si | Identificador unico del documento. |
| `patientId` | `wearable_logs`, `activity_logs` | number | Si | Identificador del paciente relacionado. |
| `deviceId` | `wearable_logs` | number | Si | Identificador del dispositivo wearable. |
| `eventType` | `wearable_logs` | string | Si | Tipo de evento capturado. |
| `payload` | `wearable_logs` | object | Si | Contenedor de mediciones flexibles. |
| `heartRate` | `wearable_logs.payload` | number | No | Ritmo cardiaco registrado. |
| `steps` | `wearable_logs.payload` | number | No | Cantidad de pasos registrados. |
| `oxygenLevel` | `wearable_logs.payload` | number | No | Nivel de oxigenacion. |
| `sleepMinutes` | `wearable_logs.payload` | number | No | Minutos de sueno registrados. |
| `activityType` | `activity_logs` | string | Si | Tipo de actividad o disciplina. |
| `value` | `activity_logs` | number | Si | Valor registrado para la actividad. |
| `unit` | `activity_logs` | string | No | Unidad del valor registrado. |
| `streakCandidate` | `activity_logs` | boolean | No | Indica si cuenta para evaluacion de racha. |
| `endpoint` | `api_audit_logs` | string | Si | Ruta consumida en la API. |
| `method` | `api_audit_logs` | string | Si | Metodo HTTP utilizado. |
| `statusCode` | `api_audit_logs` | number | Si | Codigo de respuesta HTTP. |
| `responseTimeMs` | `api_audit_logs` | number | No | Tiempo de respuesta en milisegundos. |
| `createdAt` | Todas | ISODate | Si | Fecha de creacion del documento. |

## Uso analitico

Los documentos NoSQL permiten:

- analizar comportamiento por paciente;
- consultar series de tiempo de biometria;
- detectar eventos fuera de rango;
- medir rendimiento de endpoints;
- generar datasets para modelos supervisados o no supervisados.

## Estado

Diccionario base preparado para documentar colecciones NoSQL.
