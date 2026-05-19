# Schemas NoSQL

## Descripcion general

Esta carpeta contiene los schemas propuestos para la base de datos NoSQL del proyecto **PC-Hospital-MD-Quantify**. Su objetivo es documentar la estructura esperada de colecciones usadas para almacenar informacion flexible, historica o de alta frecuencia.

## Colecciones propuestas

| Coleccion | Proposito |
| --- | --- |
| `wearable_logs` | Guardar eventos y mediciones provenientes de dispositivos wearable. |
| `activity_logs` | Registrar actividad diaria, disciplina y comportamiento del paciente. |
| `api_audit_logs` | Guardar evidencia tecnica de consumo de endpoints y rendimiento de la API. |

## Schema `wearable_logs`

```json
{
  "_id": "ObjectId",
  "patientId": "number",
  "deviceId": "number",
  "eventType": "string",
  "payload": {
    "heartRate": "number",
    "steps": "number",
    "oxygenLevel": "number",
    "sleepMinutes": "number"
  },
  "source": "WearableApp",
  "capturedAt": "ISODate",
  "createdAt": "ISODate"
}
```

## Schema `activity_logs`

```json
{
  "_id": "ObjectId",
  "patientId": "number",
  "activityType": "string",
  "value": "number",
  "unit": "string",
  "notes": "string",
  "streakCandidate": "boolean",
  "recordedAt": "ISODate"
}
```

## Schema `api_audit_logs`

```json
{
  "_id": "ObjectId",
  "userId": "number",
  "endpoint": "string",
  "method": "string",
  "statusCode": "number",
  "responseTimeMs": "number",
  "ip": "string",
  "createdAt": "ISODate"
}
```

## Reglas recomendadas

- Guardar fechas en formato ISODate.
- Mantener identificadores compatibles con la base SQL cuando exista relacion logica.
- Evitar almacenar contrasenas, tokens completos o datos sensibles sin proteccion.
- Indexar campos como `patientId`, `deviceId`, `capturedAt` y `createdAt`.

## Estado

Schemas base preparados para el modulo NoSQL.
