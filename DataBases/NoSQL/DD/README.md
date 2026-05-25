# DD — Diccionario de Datos NoSQL (MongoDB)

> **Proyecto:** PC-Hospital-MD-Quantify  
> **Motor:** MongoDB 7.0+ / Motor async  
> **Colecciones:** `logs_auditoria`, `telemetria_sesion`, `valoraciones_flexibles`  
> **Versión:** 2.0.0

---

## 1. Descripción General

El **Diccionario de Datos NoSQL** documenta las tres colecciones MongoDB del subsistema NoSQL de `PC-Hospital-MD-Quantify`: campos, tipos de dato BSON, restricciones, índices TTL y reglas de inserción.

A diferencia del DD SQL, los documentos MongoDB son schema-less por naturaleza. Sin embargo, la API aplica validación Pydantic antes de insertar, garantizando consistencia en los campos obligatorios.

---

## 2. Colección: `logs_auditoria`

**Descripción:** Registro de auditoría inmutable de todas las operaciones del sistema. Solo lectura post-inserción.

**Política de retención:** 90 días (índice TTL sobre `timestamp`).

### Campos

| Campo | Tipo BSON | Requerido | Descripción |
| :--- | :--- | :---: | :--- |
| `_id` | ObjectId | ✅ | Identificador único. Auto-generado por MongoDB |
| `correlacion_id` | String | ❌ | UUID v4 para tracing distribuido entre microservicios |
| `usuario_id` | Int32 | ✅ | ID del usuario en MySQL (`md_usuarios.id`) |
| `username` | String | ✅ | Username desnormalizado para consultas rápidas sin JOIN |
| `ip_address` | String | ✅ | Dirección IP del cliente (IPv4 o IPv6) |
| `user_agent` | String | ❌ | Cadena User-Agent del cliente HTTP |
| `accion` | String (enum) | ✅ | Tipo de operación registrada (ver tabla de valores) |
| `entidad_afectada.tipo` | String | ❌ | Tipo de entidad: `paciente`, `nota_medica`, `diagnostico`... |
| `entidad_afectada.id` | Int32 | ❌ | ID del registro SQL afectado |
| `entidad_afectada.tabla` | String | ❌ | Nombre de tabla MySQL afectada |
| `cambios.antes` | Document | ❌ | Snapshot del estado previo (solo en UPDATE/DELETE) |
| `cambios.despues` | Document | ❌ | Snapshot del estado nuevo (solo en CREATE/UPDATE) |
| `resultado` | String (enum) | ✅ | `EXITO`, `FALLIDO`, `PARCIAL`, `ROLLBACK` |
| `codigo_http` | Int32 | ❌ | Código HTTP retornado (200, 201, 409, 500...) |
| `mensaje_error` | String | ❌ | Descripción del error (si `resultado != "EXITO"`) |
| `timestamp` | Date | ✅ | Fecha/hora UTC del evento. Indexado para TTL |
| `nivel` | String (enum) | ✅ | `INFO`, `ADVERTENCIA`, `ERROR`, `EMERGENCIA` |

### Valores del campo `accion`

| Valor | Descripción |
| :--- | :--- |
| `LOGIN` | Inicio de sesión exitoso |
| `LOGOUT` | Cierre de sesión por el usuario |
| `LOGIN_FAILED` | Intento de login fallido (credenciales inválidas) |
| `CREATE_PACIENTE` | Registro de nuevo paciente |
| `UPDATE_PACIENTE` | Modificación de datos del paciente |
| `DELETE_PACIENTE` | Eliminación de paciente (soft delete) |
| `CREATE_NOTA` | Creación de nota médica |
| `CREATE_DIAGNOSTICO` | Registro de diagnóstico |
| `CREATE_TRATAMIENTO` | Prescripción de tratamiento |
| `CREATE_SIGNOS` | Registro de signos vitales |
| `CREATE_VALORACION` | Registro de escala clínica |
| `VIEW_EXPEDIENTE` | Consulta de expediente completo |
| `EXPORT_REPORTE` | Exportación de reporte epidemiológico |
| `TRANSACTION_ROLLBACK` | Rollback de transacción SQL |
| `ALERT_TRIGGERED` | Activación de alerta clínica automática |
| `UNAUTHORIZED_ACCESS` | Intento de acceso no autorizado |

### Índices

| Nombre | Campos | Tipo | Propósito |
| :--- | :--- | :--- | :--- |
| `idx_log_timestamp` | `timestamp DESC` | Simple | Consultas por rango de fecha |
| `idx_log_usuario` | `usuario_id ASC, timestamp DESC` | Compuesto | Actividad por usuario |
| `idx_log_accion` | `accion ASC` | Simple | Filtrar por tipo de operación |
| `idx_log_nivel` | `nivel ASC` | Simple | Filtrar errores/emergencias |
| `idx_log_entidad` | `entidad_afectada.tipo, entidad_afectada.id` | Compuesto | Historial de un registro |
| `idx_log_correlacion` | `correlacion_id` | Único Sparse | Tracing distribuido |

---

## 3. Colección: `telemetria_sesion`

**Descripción:** Métricas de uso y actividad de sesiones de usuario. Permite análisis de patrones de uso por turno, área y endpoint.

**Política de retención:** 180 días (configurado como TTL o limpieza batch).

### Campos

| Campo | Tipo BSON | Requerido | Descripción |
| :--- | :--- | :---: | :--- |
| `_id` | ObjectId | ✅ | Identificador único. Auto-generado |
| `token_jti` | String | ✅ | JWT ID del token (`jti` claim). Único por sesión |
| `usuario_id` | Int32 | ✅ | FK referencia a `md_usuarios.id` en MySQL |
| `username` | String | ✅ | Username del usuario autenticado |
| `rol` | String (enum) | ✅ | `admin`, `medico`, `enfermero` |
| `inicio_sesion` | Date | ✅ | Timestamp de autenticación exitosa (UTC) |
| `fin_sesion` | Date | ❌ | Null mientras sesión activa. Rellenado al cerrar |
| `duracion_segundos` | Int32 | ❌ | Calculado: `fin_sesion - inicio_sesion` |
| `ip_address` | String | ✅ | IP del cliente en el momento del login |
| `dispositivo` | String | ❌ | `desktop`, `mobile`, `tablet` |
| `requests_totales` | Int32 | ❌ | Conteo total de requests en la sesión. Default: 0 |
| `endpoints_visitados` | Array | ❌ | Lista de endpoints con métricas (ver sub-documento) |
| `endpoints_visitados[].endpoint` | String | — | Ruta del endpoint. Ej: `POST /notas-medicas` |
| `endpoints_visitados[].metodo` | String | — | Verbo HTTP: `GET`, `POST`, `PUT`, `DELETE` |
| `endpoints_visitados[].conteo` | Int32 | — | Número de veces que se invocó |
| `endpoints_visitados[].latencia_promedio_ms` | Double | — | Latencia promedio en milisegundos |
| `turno` | String (enum) | ❌ | `matutino` (7-15h), `vespertino` (15-23h), `nocturno` (23-7h) |
| `area_clinica` | String | ❌ | Área donde trabaja el usuario (ej: `urgencias`, `UCI`) |
| `estado` | String (enum) | ✅ | `activa`, `cerrada`, `expirada`, `invalidada` |
| `cerrado_por` | String (enum) | ❌ | `usuario`, `expiracion`, `admin`, `timeout` |
| `createdAt` | Date | ✅ | Timestamp de creación del documento |
| `updatedAt` | Date | ✅ | Timestamp de última actualización |

### Valores del campo `estado`

| Valor | Descripción |
| :--- | :--- |
| `activa` | Sesión JWT vigente, usuario activo |
| `cerrada` | Usuario hizo logout explícito |
| `expirada` | Token JWT llegó a su `exp` claim |
| `invalidada` | Invalidada por un administrador (blacklist) |

### Índices

| Nombre | Campos | Tipo | Propósito |
| :--- | :--- | :--- | :--- |
| `idx_tel_jti` | `token_jti` | Único | Búsqueda por token JWT |
| `idx_tel_usuario` | `usuario_id, inicio_sesion DESC` | Compuesto | Historial de sesiones por usuario |
| `idx_tel_estado` | `estado` | Simple | Filtrar sesiones activas vs. cerradas |
| `idx_tel_inicio` | `inicio_sesion DESC` | Simple | Sesiones recientes |
| `idx_tel_turno` | `turno, area_clinica` | Compuesto | Análisis de uso por turno/área |

---

## 4. Colección: `valoraciones_flexibles`

**Descripción:** Almacén de evaluaciones clínicas con estructura variable por tipo de escala. También contiene alertas vitales automáticas y advertencias de interacciones farmacológicas.

**Política de retención:** TTL de 24–72h para alertas activas (campo `expira_en`). Las valoraciones clínicas permanentes no tienen TTL.

### Campos Base (comunes a todos los tipos)

| Campo | Tipo BSON | Requerido | Descripción |
| :--- | :--- | :---: | :--- |
| `_id` | ObjectId | ✅ | Identificador único. Auto-generado |
| `paciente_id` | Int32 | ✅ | FK referencia a `md_pacientes.id` en MySQL |
| `valoracion_sql_id` | Int32 | ❌ | FK opcional a `md_valoraciones.id` en MySQL |
| `registrado_por_id` | Int32 | ❌ | FK referencia a `md_usuarios.id` |
| `tipo` | String (enum) | ✅ | Tipo de valoración o alerta (ver tabla de tipos) |
| `nivel` | String (enum) | ✅ | `NORMAL`, `BAJO`, `MODERADO`, `ALTO`, `CRITICO`, `EMERGENCIA` |
| `componentes` | Document (Mixed) | ❌ | Estructura variable según `tipo` |
| `total` | Double | ❌ | Puntaje numérico total (null para alertas no escaladas) |
| `interpretacion` | String | ❌ | Texto de interpretación clínica automatizada |
| `requiere_intervencion` | Boolean | ✅ | `true` = requiere acción inmediata del personal |
| `accion_tomada` | String | ❌ | Descripción de la acción clínica tomada |
| `notificado` | Boolean | ✅ | `true` = personal notificado |
| `timestamp` | Date | ✅ | Fecha/hora UTC del evento |
| `expira_en` | Date | ❌ | TTL para documentos de alerta temporal (índice TTL) |

### Tipos y estructura de `componentes`

#### Tipo `Glasgow`

```json
"componentes": {
  "apertura_ocular": { "valor": 1–4, "descripcion": "..." },
  "respuesta_verbal": { "valor": 1–5, "descripcion": "..." },
  "respuesta_motora": { "valor": 1–6, "descripcion": "..." }
}
```
**Total:** suma de los tres componentes (3–15 pts)

#### Tipo `MEWS`

```json
"componentes": {
  "frecuencia_cardiaca_pts": 0–2,
  "frecuencia_respiratoria_pts": 0–3,
  "saturacion_o2_pts": 0–3,
  "temperatura_pts": 0–2,
  "consciencia_pts": 0–3,
  "valores_raw": {
    "fc": 95, "fr": 18, "spo2": 97, "temp": 37.2, "consciencia": "alerta"
  }
}
```
**Total:** suma de puntos por parámetro (0–14 pts)

#### Tipo `APGAR`

```json
"componentes": {
  "apariencia": { "valor": 0–2, "descripcion": "..." },
  "pulso": { "valor": 0–2, "descripcion": "..." },
  "gesticulacion": { "valor": 0–2, "descripcion": "..." },
  "actividad": { "valor": 0–2, "descripcion": "..." },
  "respiracion": { "valor": 0–2, "descripcion": "..." },
  "minuto_evaluacion": 1
}
```
**Total:** suma de los cinco componentes (0–10 pts)

#### Tipo `alerta_vital`

```json
"componentes": {
  "parametros_violados": [
    { "campo": "...", "valor_real": 155, "umbral": "> 150", "puntos_mews": 2 }
  ],
  "score_mews": 9,
  "mews_previo": 3,
  "tipo_alerta": "CODIGO_AZUL"
}
```

#### Tipo `interaccion_farmacologica`

```json
"componentes": {
  "medicamento_activo": "Enalapril 10mg",
  "medicamento_nuevo": "Ibuprofeno 400mg",
  "mecanismo": "...",
  "referencia": "Micromedex 2.0",
  "severidad_interaccion": "Mayor",
  "alternativas_sugeridas": ["..."]
}
```

### Niveles de Clasificación por Escala

| Escala | Nivel NORMAL | Nivel MODERADO | Nivel CRITICO |
| :--- | :--- | :--- | :--- |
| Glasgow | 13–15 | 9–12 | ≤ 8 |
| MEWS | 0–4 | 5–6 | ≥ 7 |
| APGAR | 7–10 | 4–6 | ≤ 3 |
| `alerta_vital` | — | 1–2 param. violados | ≥ 3 param. violados |
| `interaccion_farmacologica` | — | Moderada | Mayor/Contraindicada |

### Índices

| Nombre | Campos | Tipo | Propósito |
| :--- | :--- | :--- | :--- |
| `idx_val_paciente` | `paciente_id, timestamp DESC` | Compuesto | Historial del paciente |
| `idx_val_tipo` | `tipo` | Simple | Consultas por tipo de escala |
| `idx_val_nivel` | `nivel` | Simple | Alertas críticas activas |
| `idx_val_timestamp` | `timestamp DESC` | Simple | Ordenamiento temporal |
| `idx_val_intervencion` | `requiere_intervencion` | Simple | Dashboard de emergencias |
| `idx_val_ttl` | `expira_en` | TTL | Expiración automática de alertas temporales |

---

## 5. Convenciones de Nomenclatura

| Elemento | Convención | Ejemplo |
| :--- | :--- | :--- |
| Nombres de colecciones | `snake_case` plural | `logs_auditoria` |
| Campos de documento | `snake_case` | `usuario_id`, `ip_address` |
| Nombres de índices | `idx_coleccion_campo` | `idx_log_timestamp` |
| Referencias SQL | Sufijo `_id` + comentario | `usuario_id` // FK md_usuarios |
| Enumeraciones | `UPPER_CASE` (niveles) o `lower_case` (valores) | `CRITICO`, `medico` |

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |  Revisado y Aprobado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En Revision |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En Revision |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |
