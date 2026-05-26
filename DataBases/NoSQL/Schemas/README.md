# Schemas — Esquemas NoSQL (MongoDB)

> **Proyecto:** PC-Hospital-MD-Quantify  
> **Motor:** MongoDB 7.0+ / Motor (async Python driver)  
> **Colecciones:** `logs_auditoria`, `telemetria_sesion`, `valoraciones_flexibles`  
> **Versión:** 2.0.0

---

## 1. Descripción General

Este documento define los **esquemas de documento** para las tres colecciones MongoDB del subsistema NoSQL de `PC-Hospital-MD-Quantify`. El enfoque híbrido permite usar MongoDB para datos que requieren flexibilidad de estructura, trazabilidad de eventos, y análisis de telemetría — mientras que los datos estructurados y transaccionales se mantienen en MySQL.

### Arquitectura híbrida

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI (Motor)                    │
├─────────────────┬───────────────────────────────────┤
│   MySQL (SQL)   │        MongoDB (NoSQL)              │
│─────────────────│─────────────────────────────────────│
│ md_pacientes    │ logs_auditoria                      │
│ md_notas_medicas│ telemetria_sesion                   │
│ md_diagnostico  │ valoraciones_flexibles              │
│ md_tratamientos │                                     │
│ md_signos_vitales│                                   │
└─────────────────┴───────────────────────────────────┘
```

---

## 2. Colección: `logs_auditoria`

**Propósito:** Trazabilidad completa de todas las operaciones del sistema (creación, modificación, eliminación, errores, rollbacks). Inmutable — los documentos nunca se modifican, solo se insertan.

### 2.1 Schema (Mongoose / JSON Schema)

```javascript
const LogAuditoriaSchema = new Schema({
  // Identificadores
  _id: ObjectId,                          // Auto-generado por MongoDB
  correlacion_id: String,                 // UUID para tracing distribuido

  // Actor
  usuario_id: Number,                     // FK -> md_usuarios.id (referencia SQL)
  username: String,                       // Desnormalizado para velocidad
  ip_address: String,                     // IPv4 o IPv6 del cliente
  user_agent: String,                     // Browser/cliente HTTP

  // Evento
  accion: {
    type: String,
    enum: [
      "LOGIN", "LOGOUT", "LOGIN_FAILED",
      "CREATE_PACIENTE", "UPDATE_PACIENTE", "DELETE_PACIENTE",
      "CREATE_NOTA", "CREATE_DIAGNOSTICO", "CREATE_TRATAMIENTO",
      "CREATE_SIGNOS", "CREATE_VALORACION",
      "VIEW_EXPEDIENTE", "EXPORT_REPORTE",
      "TRANSACTION_ROLLBACK", "ALERT_TRIGGERED",
      "UNAUTHORIZED_ACCESS"
    ],
    required: true
  },

  // Contexto de la operación
  entidad_afectada: {
    tipo: String,   // "paciente", "nota_medica", "diagnostico", etc.
    id: Number,     // ID del registro SQL afectado
    tabla: String   // Nombre exacto de la tabla MySQL
  },

  // Datos del cambio (para operaciones de escritura)
  cambios: {
    antes: Mixed,   // Estado previo (en actualizaciones/eliminaciones)
    despues: Mixed  // Estado nuevo (en creaciones/actualizaciones)
  },

  // Estado
  resultado: {
    type: String,
    enum: ["EXITO", "FALLIDO", "PARCIAL", "ROLLBACK"],
    required: true
  },
  codigo_http: Number,           // HTTP status retornado (200, 201, 409, etc.)
  mensaje_error: String,         // Solo si resultado != "EXITO"

  // Temporalidad
  timestamp: { type: Date, default: Date.now, index: true },
  nivel: {
    type: String,
    enum: ["INFO", "ADVERTENCIA", "ERROR", "EMERGENCIA"],
    default: "INFO"
  }
}, {
  collection: "logs_auditoria",
  timestamps: false  // Manejamos timestamp manualmente
});

// Índices
LogAuditoriaSchema.index({ timestamp: -1 });          // Consulta por fecha desc
LogAuditoriaSchema.index({ usuario_id: 1, timestamp: -1 }); // Por usuario
LogAuditoriaSchema.index({ accion: 1 });              // Por tipo de acción
LogAuditoriaSchema.index({ nivel: 1 });               // Filtrar errores
LogAuditoriaSchema.index({ "entidad_afectada.tipo": 1, "entidad_afectada.id": 1 });
LogAuditoriaSchema.index({ correlacion_id: 1 }, { unique: true, sparse: true });
```

### 2.2 Ejemplo de Documento

```json
{
  "_id": {"$oid": "6650a1b2c3d4e5f678901234"},
  "correlacion_id": "txn-2026-05-21-a7f9b3",
  "usuario_id": 3,
  "username": "dr.garcia",
  "ip_address": "192.168.1.45",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0) FastAPI-Client/2.0",
  "accion": "CREATE_NOTA",
  "entidad_afectada": {
    "tipo": "nota_medica",
    "id": 128,
    "tabla": "md_notas_medicas"
  },
  "cambios": {
    "antes": null,
    "despues": {
      "paciente_id": 7,
      "tipo_nota": "evolucion",
      "fecha": "2026-05-21T10:00:00"
    }
  },
  "resultado": "EXITO",
  "codigo_http": 201,
  "mensaje_error": null,
  "timestamp": {"$date": "2026-05-21T10:00:01.234Z"},
  "nivel": "INFO"
}
```

---

## 3. Colección: `telemetria_sesion`

**Propósito:** Métricas de sesiones de usuario — duración, endpoints más usados, actividad por turno, latencias. Permite análisis de uso para optimización y auditoría de acceso.

### 3.1 Schema

```javascript
const TelemetriaSesionSchema = new Schema({
  _id: ObjectId,
  token_jti: String,            // JWT ID (jti claim) — identificador único del token

  // Usuario
  usuario_id: Number,           // FK -> md_usuarios.id
  username: String,
  rol: { type: String, enum: ["admin", "medico", "enfermero"] },

  // Sesión
  inicio_sesion: { type: Date, required: true },
  fin_sesion: Date,             // Null si sesión activa
  duracion_segundos: Number,    // Calculado al cerrar sesión
  ip_address: String,
  dispositivo: String,          // "desktop", "mobile", "tablet"

  // Actividad de la sesión
  requests_totales: { type: Number, default: 0 },
  endpoints_visitados: [{
    endpoint: String,            // Ej: "POST /notas-medicas"
    metodo: String,              // GET, POST, PUT, DELETE
    conteo: Number,
    latencia_promedio_ms: Number
  }],

  // Contexto hospitalario
  turno: {
    type: String,
    enum: ["matutino", "vespertino", "nocturno"]
  },
  area_clinica: String,         // "urgencias", "UCI", "medicina_interna"

  // Estado
  estado: {
    type: String,
    enum: ["activa", "cerrada", "expirada", "invalidada"],
    default: "activa"
  },
  cerrado_por: {
    type: String,
    enum: ["usuario", "expiracion", "admin", "timeout"],
  },

  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
}, { collection: "telemetria_sesion" });

TelemetriaSesionSchema.index({ token_jti: 1 }, { unique: true });
TelemetriaSesionSchema.index({ usuario_id: 1, inicio_sesion: -1 });
TelemetriaSesionSchema.index({ estado: 1 });
TelemetriaSesionSchema.index({ inicio_sesion: -1 });
TelemetriaSesionSchema.index({ turno: 1, area_clinica: 1 });
```

### 3.2 Ejemplo de Documento

```json
{
  "_id": {"$oid": "6650b2c3d4e5f67890125678"},
  "token_jti": "jti-abc123-def456",
  "usuario_id": 2,
  "username": "dra.lopez",
  "rol": "medico",
  "inicio_sesion": {"$date": "2026-05-21T07:00:00.000Z"},
  "fin_sesion": {"$date": "2026-05-21T15:00:00.000Z"},
  "duracion_segundos": 28800,
  "ip_address": "10.0.1.22",
  "dispositivo": "desktop",
  "requests_totales": 142,
  "endpoints_visitados": [
    {"endpoint": "GET /pacientes/{id}/expediente", "metodo": "GET", "conteo": 45, "latencia_promedio_ms": 320},
    {"endpoint": "POST /notas-medicas", "metodo": "POST", "conteo": 12, "latencia_promedio_ms": 85},
    {"endpoint": "POST /signos-vitales", "metodo": "POST", "conteo": 38, "latencia_promedio_ms": 60}
  ],
  "turno": "matutino",
  "area_clinica": "medicina_interna",
  "estado": "cerrada",
  "cerrado_por": "usuario",
  "createdAt": {"$date": "2026-05-21T07:00:00.000Z"},
  "updatedAt": {"$date": "2026-05-21T15:00:02.000Z"}
}
```

---

## 4. Colección: `valoraciones_flexibles`

**Propósito:** Almacenar el detalle completo de escalas clínicas con estructura variable por tipo de escala. El campo `componentes` es diferente para cada escala, lo que hace que MongoDB sea ideal para este caso.

### 4.1 Schema

```javascript
const ValoracionFlexibleSchema = new Schema({
  _id: ObjectId,
  
  // Referencia SQL
  paciente_id: { type: Number, required: true, index: true },
  valoracion_sql_id: Number,        // FK -> md_valoraciones.id (si existe)
  registrado_por_id: Number,        // FK -> md_usuarios.id

  // Tipo de escala
  tipo: {
    type: String,
    required: true,
    enum: ["Glasgow", "MEWS", "APGAR", "Braden", "Norton", "SOFA",
           "interaccion_farmacologica", "alerta_clinica", "alerta_vital"]
  },

  // Clasificación de severidad
  nivel: {
    type: String,
    enum: ["NORMAL", "BAJO", "MODERADO", "ALTO", "CRITICO", "EMERGENCIA"],
    required: true
  },

  // Componentes variables según el tipo de escala
  componentes: Mixed,              // Schema-less — diferente por cada tipo

  // Resultado
  total: Number,                   // Puntaje total calculado
  interpretacion: String,          // Texto de interpretación clínica
  
  // Alertas y acciones
  requiere_intervencion: { type: Boolean, default: false },
  accion_tomada: String,           // Ej: "Traslado a UCI", "Código Azul activado"
  notificado: { type: Boolean, default: false },
  
  // Temporalidad
  timestamp: { type: Date, default: Date.now, index: true },
  expira_en: Date                  // Para alertas temporales (ej: 24h)
}, { collection: "valoraciones_flexibles" });

ValoracionFlexibleSchema.index({ paciente_id: 1, timestamp: -1 });
ValoracionFlexibleSchema.index({ tipo: 1 });
ValoracionFlexibleSchema.index({ nivel: 1 });
ValoracionFlexibleSchema.index({ timestamp: -1 });
ValoracionFlexibleSchema.index({ requiere_intervencion: 1 });
ValoracionFlexibleSchema.index({ expira_en: 1 }, { expireAfterSeconds: 0 }); // TTL Index
```

### 4.2 Ejemplos de Documentos por Tipo

**Escala Glasgow:**
```json
{
  "paciente_id": 14,
  "tipo": "Glasgow",
  "nivel": "CRITICO",
  "componentes": {
    "apertura_ocular": { "valor": 2, "descripcion": "Al dolor" },
    "respuesta_verbal": { "valor": 2, "descripcion": "Sonidos incomprensibles" },
    "respuesta_motora": { "valor": 4, "descripcion": "Retirada al dolor" }
  },
  "total": 8,
  "interpretacion": "TEC Severo — GCS ≤ 8. Requiere intubación y UCI.",
  "requiere_intervencion": true,
  "accion_tomada": "Activado protocolo UCI. Interconsulta a neurocirugía.",
  "notificado": true,
  "timestamp": {"$date": "2026-05-21T15:00:00.000Z"}
}
```

**Alerta Vital (Código Azul):**
```json
{
  "paciente_id": 11,
  "tipo": "alerta_vital",
  "nivel": "EMERGENCIA",
  "componentes": {
    "parametros_violados": [
      {"campo": "frecuencia_cardiaca", "valor_real": 155, "umbral": "> 150"},
      {"campo": "saturacion_o2", "valor_real": 83, "umbral": "< 90%"},
      {"campo": "tension_arterial_sistolica", "valor_real": 68, "umbral": "< 80 mmHg"},
      {"campo": "frecuencia_respiratoria", "valor_real": 34, "umbral": "> 30"}
    ],
    "score_mews": 9,
    "mews_previo": 3
  },
  "total": 9,
  "interpretacion": "Deterioro súbito. 4 parámetros críticos simultáneos. CÓDIGO AZUL.",
  "requiere_intervencion": true,
  "accion_tomada": "CODIGO_AZUL activado. Equipo de reanimación notificado.",
  "notificado": true,
  "timestamp": {"$date": "2026-05-21T14:22:01.500Z"},
  "expira_en": {"$date": "2026-05-22T14:22:01.500Z"}
}
```

**Interacción Farmacológica:**
```json
{
  "paciente_id": 5,
  "tipo": "interaccion_farmacologica",
  "nivel": "ALTO",
  "componentes": {
    "medicamento_activo": "Enalapril 10mg",
    "medicamento_nuevo": "Ibuprofeno 400mg",
    "mecanismo": "Los AINEs reducen el efecto antihipertensivo de los IECA y pueden deteriorar la función renal",
    "referencia": "Micromedex 2.0 — Interacción Moderada-Mayor",
    "alternativas_sugeridas": ["Paracetamol 500mg", "Metamizol 575mg"]
  },
  "total": null,
  "interpretacion": "Interacción AINE + IECA. Riesgo renal y cardiovascular aumentado.",
  "requiere_intervencion": false,
  "accion_tomada": "Advertencia mostrada al médico. Prescripción forzada con firma de confirmación.",
  "notificado": true,
  "timestamp": {"$date": "2026-05-21T11:30:00.000Z"}
}
```

---

## 5. Conexión Motor (FastAPI async)

```python
# mongo_database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING

MONGO_URL = "mongodb://localhost:27017"
MONGO_DB = "quantify_nosql"

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

# Colecciones
logs_auditoria = db["logs_auditoria"]
telemetria_sesion = db["telemetria_sesion"]
valoraciones_flexibles = db["valoraciones_flexibles"]

async def init_mongo_indexes():
    """Crear índices al iniciar la aplicación."""
    await logs_auditoria.create_indexes([
        IndexModel([("timestamp", DESCENDING)]),
        IndexModel([("usuario_id", ASCENDING), ("timestamp", DESCENDING)]),
        IndexModel([("accion", ASCENDING)]),
        IndexModel([("nivel", ASCENDING)]),
    ])
    await telemetria_sesion.create_indexes([
        IndexModel([("token_jti", ASCENDING)], unique=True),
        IndexModel([("usuario_id", ASCENDING), ("inicio_sesion", DESCENDING)]),
        IndexModel([("estado", ASCENDING)]),
    ])
    await valoraciones_flexibles.create_indexes([
        IndexModel([("paciente_id", ASCENDING), ("timestamp", DESCENDING)]),
        IndexModel([("tipo", ASCENDING)]),
        IndexModel([("nivel", ASCENDING)]),
        IndexModel([("expira_en", ASCENDING)], expireAfterSeconds=0),
    ])
```

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |  Revisado y Aprobado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En Revision |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |
