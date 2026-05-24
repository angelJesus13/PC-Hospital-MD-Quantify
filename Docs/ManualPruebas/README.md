# Manual de Pruebas Base de Simulación — UDN (PC-Hospital-MD-Quantify)

> **Versión:** 2.0.0  
> **Proyecto:** PC-Hospital-MD-Quantify  
> **Módulo:** Unidad de Desarrollo de Negocio (UDN)  
> **API de Referencia:** [MEDICAL_REGISTER_API](https://github.com/AngelJdev/MEDICAL_REGISTER_API)  
> **Framework:** FastAPI + SQLAlchemy (MySQL) + Motor (MongoDB)

---

## 1. Introducción

Este documento constituye el **Manual de Pruebas Base de Simulación** para la Unidad de Desarrollo de Negocio (UDN) del proyecto `PC-Hospital-MD-Quantify`. Contiene **10 escenarios clínicos específicos** diseñados para validar el comportamiento integral de la plataforma bajo condiciones operativas reales de un entorno hospitalario híbrido (SQL + NoSQL).

Las pruebas están directamente alineadas con la arquitectura técnica de la API: modelos relacionales MySQL administrados mediante SQLAlchemy, validaciones Pydantic, autenticación JWT con roles, y colecciones MongoDB para logs de auditoría, telemetría y valoraciones flexibles.

---

## 2. Objetivo

Validar funcionalidades críticas del sistema mediante pruebas de simulación que reproduzcan condiciones operativas reales, garantizando:

- Exactitud en el registro, consulta y modificación de datos clínicos.
- Integridad referencial entre entidades relacionales (pacientes, notas, diagnósticos, tratamientos).
- Correcto disparo de alertas clínicas y reglas de priorización.
- Seguridad transaccional bajo autenticación JWT con diferenciación de roles.
- Consistencia entre el motor SQL y las colecciones MongoDB bajo carga concurrente.

---

## 3. Alcance

| Capa | Componentes cubiertos |
| :--- | :--- |
| **API REST** | Endpoints FastAPI: `/pacientes`, `/notas-medicas`, `/signos-vitales`, `/diagnostico`, `/tratamientos`, `/valoraciones`, `/auditoria`, `/telemetria` |
| **Base de datos SQL** | 12 tablas: `md_usuarios`, `md_pacientes`, `md_notas_medicas`, `md_signos_vitales`, `md_diagnostico`, `md_tratamientos`, `md_nacimientos`, `md_defunciones`, `md_documentos_oficiales`, `md_domicilios`, `md_personas_tiene_domicilio`, `md_valoraciones` |
| **Base de datos NoSQL** | Colecciones: `logs_auditoria`, `telemetria_sesion`, `valoraciones_flexibles` |
| **Seguridad** | JWT (HS256), bcrypt password hashing, guards de rol: `admin`, `medico` |
| **Simulación UDN** | Motor de decisión clínica: alertas, priorización, escalas de valoración |

> **Fuera de alcance:** Integración con hardware físico de monitoreo, pruebas de carga > 500 usuarios concurrentes, interfaces gráficas de usuario final.

---

## 4. Metodología de Prueba

```
Preparación → Ejecución → Observación → Documentación → Seguimiento
```

1. **Preparación:** Cargar datos de prueba con `seed_db.py`. Verificar conectividad SQL y MongoDB. Obtener token JWT de rol correspondiente.
2. **Ejecución:** Realizar peticiones HTTP (REST) según la secuencia descrita. Registrar payloads, respuestas y métricas.
3. **Observación:** Comparar respuesta real contra resultado esperado. Revisar logs en MongoDB y estado SQL.
4. **Documentación:** Llenar la tabla de registro correspondiente a cada prueba.
5. **Seguimiento:** Abrir issues en el repositorio por cada desviación encontrada.

---

## 5. Convenciones

| Término | Definición |
| :--- | :--- |
| `Escenario` | Contexto clínico específico que se está simulando |
| `Entidades involucradas` | Tablas SQL y/o colecciones MongoDB que participan |
| `Entrada` | Payload JSON o condiciones previas requeridas |
| `Acción` | Secuencia de requests HTTP a ejecutar |
| `Métrica esperada` | Valor numérico o condición clínica esperada |
| `Resultado esperado` | Comportamiento correcto del sistema |
| `Criterio de aprobación` | Umbral mínimo para marcar la prueba como ✅ Aprobada |
| `Estado` | ✅ Aprobada / ❌ Rechazada / ⚠️ Observación |

---

## 6. Pruebas Específicas de la UDN

---

### Prueba 1: Simulación de Registro Masivo y Validación de Identidad de Pacientes

**Escenario clínico:** El hospital recibe un convoy de 15 pacientes procedentes de una zona de emergencia. Se deben registrar todos en el sistema en menos de 5 minutos, verificando unicidad de CURP y vinculando domicilios correctamente.

**Entidades involucradas:** `md_pacientes`, `md_domicilios`, `md_personas_tiene_domicilio`, `logs_auditoria` (MongoDB)

**Entrada:**
```json
POST /pacientes
{
  "nombre": "María Luisa Hernández Torres",
  "curp": "HETM850312MDFRRR01",
  "fecha_registro": "2026-05-21T08:30:00"
}

POST /domicilios
{
  "calle": "Av. Insurgentes 1245",
  "colonia": "Santa Fe",
  "municipio": "Álvaro Obregón",
  "estado": "CDMX",
  "cp": "01210"
}
```

**Acción:**
1. `POST /auth/login` → Obtener token JWT con rol `admin`.
2. Ejecutar 15 requests `POST /pacientes` con CURPs únicas. Inyectar 2 CURPs duplicadas para forzar error 409.
3. Ejecutar `POST /domicilios` para cada domicilio y vincular con `POST /pacientes/{id}/domicilio`.
4. Verificar log de auditoría en MongoDB: `GET /auditoria?accion=CREATE_PACIENTE`.

**Métricas esperadas:**
- 13 registros exitosos (HTTP 201), 2 rechazados por CURP duplicada (HTTP 409).
- Tiempo promedio de inserción < 200 ms por registro.
- Entrada de log por cada creación exitosa en `logs_auditoria`.

**Resultado esperado:** Sistema registra pacientes con integridad referencial completa, rechaza duplicados con mensaje claro, y persiste todos los eventos en el log de auditoría MongoDB.

**Criterio de aprobación:**
- ≥ 95% de requests procesados en < 300 ms.
- 0 registros con CURP duplicada insertados en SQL.
- Todos los eventos registrados en `logs_auditoria` con `timestamp`, `usuario_id`, `accion`, y `entidad_afectada`.

---

### Prueba 2: Simulación de Triage Clínico y Registro de Signos Vitales

**Escenario clínico:** 8 pacientes llegan simultáneamente a urgencias. La enfermera registra los signos vitales de cada uno. El sistema debe detectar automáticamente cuáles tienen signos críticos (MEWS score ≥ 5) y escalar la alerta.

**Entidades involucradas:** `md_pacientes`, `md_signos_vitales`, `valoraciones_flexibles` (MongoDB), `logs_auditoria`

**Entrada:**
```json
POST /signos-vitales
{
  "paciente_id": 7,
  "tension_arterial": "80/50",
  "frecuencia_cardiaca": 132,
  "temperatura": 38.9,
  "saturacion_o2": 88,
  "frecuencia_respiratoria": 28,
  "escala_consciencia": "confuso",
  "fecha": "2026-05-21T09:15:00"
}
```

**Acción:**
1. `POST /auth/login` → Token rol `medico`.
2. Registrar signos vitales para 8 pacientes (4 normales, 4 con parámetros críticos).
3. Sistema evalúa automáticamente score MEWS:
   - FC > 130 → +2 pts
   - SpO2 < 90% → +3 pts
   - FR > 25 → +2 pts
   - Temperatura > 38.5 → +1 pt
4. Si MEWS ≥ 5: sistema persiste alerta en `valoraciones_flexibles` MongoDB con `nivel: "CRITICO"`.
5. `GET /pacientes/{id}/alertas` → Verificar alertas activas por paciente.

**Métricas esperadas:**
- Score MEWS calculado correctamente para los 8 pacientes.
- 4 alertas críticas creadas en MongoDB con `nivel: "CRITICO"`.
- 0 alertas falsas para los 4 pacientes con signos normales.

**Resultado esperado:** Sistema registra signos vitales, calcula score en tiempo real, diferencia correctamente entre pacientes estables y críticos, y persiste alertas estructuradas en MongoDB.

**Criterio de aprobación:**
- 100% de precisión en clasificación crítica vs. estable.
- Latencia de creación de alerta < 100 ms posterior al POST de signos vitales.
- Todos los documentos en `valoraciones_flexibles` con campos: `paciente_id`, `tipo`, `nivel`, `detalles`, `timestamp`.

---

### Prueba 3: Simulación de Consulta Médica, Nota Clínica y Diagnóstico CIE-10

**Escenario clínico:** Un médico atiende a un paciente con sospecha de neumonía y debe registrar la nota médica de tipo `evolución`, vincularla a un diagnóstico con código CIE-10 (J18.9) y prescribir tratamiento.

**Entidades involucradas:** `md_notas_medicas`, `md_diagnostico`, `md_tratamientos`, `md_usuarios`, `md_pacientes`, `logs_auditoria`

**Entrada:**
```json
POST /notas-medicas
{
  "paciente_id": 3,
  "medico_id": 2,
  "tipo_nota": "evolucion",
  "contenido": "Paciente masculino de 45 años con fiebre de 5 días de evolución, tos productiva con expectoración purulenta, SpO2 91% al aire ambiente. Rx tórax con opacidad en LID compatible con neumonía. Se inicia tratamiento antibiótico empírico.",
  "fecha": "2026-05-21T10:00:00"
}

POST /diagnostico
{
  "nota_id": 12,
  "descripcion": "Neumonía, no especificada",
  "codigo_cie": "J18.9"
}

POST /tratamientos
{
  "diagnostico_id": 8,
  "medicamento": "Amoxicilina-Clavulanato",
  "dosis": "875/125 mg",
  "frecuencia": "cada 12 horas",
  "duracion": "7 días"
}
```

**Acción:**
1. `POST /auth/login` → Token rol `medico`.
2. Crear nota médica tipo `evolucion` para paciente id=3.
3. Crear diagnóstico vinculado a la nota con código CIE-10 validado.
4. Crear tratamiento vinculado al diagnóstico con todos los campos.
5. `GET /pacientes/3/expediente` → Verificar expediente completo integrado.
6. Verificar log en `logs_auditoria` con cadena: `nota → diagnóstico → tratamiento`.

**Métricas esperadas:**
- Cadena `nota_medica → diagnostico → tratamiento` íntegra y trazable.
- Código CIE-10 validado contra catálogo (no debe aceptar `ZZ9.9`).
- Expediente del paciente retorna notas, diagnósticos y tratamientos en orden cronológico.

**Resultado esperado:** El sistema permite documentar un episodio clínico completo con validación de codificación internacional, retorno estructurado del expediente, y trazabilidad completa en logs.

**Criterio de aprobación:**
- HTTP 201 en nota, diagnóstico y tratamiento.
- `GET /pacientes/3/expediente` retorna estructura anidada correcta.
- Código CIE-10 inválido retorna HTTP 422 con mensaje descriptivo.
- Log de auditoría contiene los 3 eventos en < 500 ms total.

---

### Prueba 4: Simulación de Prescripción y Detección de Interacciones Farmacológicas

**Escenario clínico:** Paciente con diagnóstico dual (hipertensión + infección bacteriana) que ya tiene tratamiento activo con `Enalapril 10mg`. El médico intenta prescribir `Ibuprofeno 400mg` — interacción conocida que puede elevar presión arterial y deteriorar función renal.

**Entidades involucradas:** `md_tratamientos`, `md_diagnostico`, `valoraciones_flexibles` (MongoDB — interacciones)

**Entrada:**
```json
POST /tratamientos
{
  "diagnostico_id": 9,
  "medicamento": "Ibuprofeno",
  "dosis": "400 mg",
  "frecuencia": "cada 8 horas",
  "duracion": "5 días"
}
```

**Acción:**
1. Obtener token JWT rol `medico`.
2. Consultar tratamientos activos del paciente: `GET /pacientes/5/tratamientos-activos`.
3. Intentar crear nuevo tratamiento con medicamento en lista de interacciones.
4. Sistema consulta colección MongoDB `valoraciones_flexibles.tipo = "interaccion_farmacologica"`.
5. Si existe interacción registrada: responder con HTTP 409 y advertencia clínica.
6. Si el médico confirma con flag `forzar_prescripcion: true`: registrar tratamiento + alerta en `logs_auditoria`.

**Métricas esperadas:**
- Interacción `Enalapril + NSAID` detectada correctamente.
- HTTP 409 con payload: `{"advertencia": "Interacción potencial: AINE puede reducir efecto antihipertensivo y comprometer función renal."}`.
- Si se fuerza prescripción: registro en SQL + documento de advertencia en MongoDB.

**Resultado esperado:** Sistema detecta interacciones farmacológicas consultando MongoDB, informa al médico con contexto clínico, y permite override documentado.

**Criterio de aprobación:**
- 100% detección de interacciones listadas en base de datos MongoDB.
- 0 prescripciones de riesgo sin advertencia registrada.
- Overhead del chequeo de interacciones < 50 ms adicionales.

---

### Prueba 5: Simulación de Alertas Clínicas Automáticas por Signos Vitales Fuera de Rango

**Escenario clínico:** Sistema de monitoreo continuo registra deterioro súbito en paciente de UCI: FC > 150 lpm, SpO2 < 85%, PA < 70/40 mmHg. Se debe activar alerta de Código Azul y notificar en tiempo real.

**Entidades involucradas:** `md_signos_vitales`, `logs_auditoria`, `valoraciones_flexibles`

**Entrada:**
```json
POST /signos-vitales
{
  "paciente_id": 11,
  "tension_arterial": "68/38",
  "frecuencia_cardiaca": 155,
  "temperatura": 35.1,
  "saturacion_o2": 83,
  "frecuencia_respiratoria": 34,
  "fecha": "2026-05-21T14:22:00"
}
```

**Acción:**
1. Registrar signos vitales con parámetros críticos múltiples.
2. Motor de reglas evalúa cada parámetro contra umbrales definidos:

| Parámetro | Rango Normal | Umbral Crítico |
| :--- | :--- | :--- |
| Frecuencia Cardíaca | 60–100 lpm | < 40 o > 150 lpm |
| SpO2 | ≥ 95% | < 90% |
| Tensión Arterial Sistólica | 90–140 mmHg | < 80 mmHg |
| Frecuencia Respiratoria | 12–20 rpm | > 30 rpm |

3. Si ≥ 3 parámetros críticos: emitir `CODIGO_AZUL` en `valoraciones_flexibles`.
4. Crear documento en `logs_auditoria` con `nivel: "EMERGENCIA"` y lista de parámetros fuera de rango.
5. `GET /pacientes/11/alertas-activas` → Retornar alertas en curso.

**Métricas esperadas:**
- `CODIGO_AZUL` activado en < 200 ms desde el POST de signos vitales.
- Documento MongoDB con todos los parámetros violados y sus valores reales.
- Endpoint de alertas activas retorna la alerta correctamente.

**Resultado esperado:** El motor de alertas actúa automáticamente sin intervención humana, clasifica la severidad correctamente y persiste el evento con trazabilidad completa.

**Criterio de aprobación:**
- 100% de alertas críticas correctamente clasificadas.
- Tiempo de activación de alerta < 200 ms.
- Documento de alerta incluye: `paciente_id`, `timestamp`, `tipo: "CODIGO_AZUL"`, `parametros_violados[]`, `notificado: true`.

---

### Prueba 6: Simulación de Escalas de Valoración Clínica de Riesgo (MEWS / Glasgow)

**Escenario clínico:** Un paciente neurológico ingresa con sospecha de TEC (traumatismo craneoencefálico). El médico aplica la Escala de Glasgow para valorar nivel de consciencia y determinar gravedad.

**Entidades involucradas:** `md_valoraciones`, `valoraciones_flexibles` (MongoDB — escala completa)

**Entrada:**
```json
POST /valoraciones
{
  "paciente_id": 14,
  "escala": "Glasgow",
  "resultado": "8",
  "observaciones": "Apertura ocular al dolor (2), Respuesta verbal incomprensible (2), Respuesta motora de flexión (4). GCS = 8. TEC severo."
}
```

**Acción:**
1. Token JWT rol `medico`.
2. Registrar valoración Glasgow en `md_valoraciones` (SQL) — resumen estructurado.
3. Registrar desglose completo en `valoraciones_flexibles` MongoDB:
```json
{
  "paciente_id": 14,
  "tipo": "Glasgow",
  "componentes": {
    "apertura_ocular": 2,
    "respuesta_verbal": 2,
    "respuesta_motora": 4
  },
  "total": 8,
  "interpretacion": "TEC Severo — Requiere UCI",
  "timestamp": "2026-05-21T15:00:00"
}
```
4. Sistema clasifica automáticamente: Glasgow ≤ 8 → `NIVEL_CRITICO`.
5. Activar protocolo UCI: añadir flag `requiere_uci: true` al registro del paciente.

**Métricas esperadas:**
- Valoración SQL registrada con suma correcta (resultado = "8").
- Documento MongoDB con componentes individuales y clasificación automática.
- Flag `requiere_uci` activado correctamente.

**Resultado esperado:** Sistema almacena tanto el resumen estructurado (SQL) como los datos ricos de la escala completa (MongoDB) y actúa según la clasificación de severidad.

**Criterio de aprobación:**
- Suma de componentes = total declarado (validación de consistencia).
- Clasificación correcta para: Glasgow ≤ 8 → CRÍTICO, 9–12 → MODERADO, 13–15 → LEVE.
- `GET /pacientes/14/valoraciones` retorna historia completa de valoraciones.

---

### Prueba 7: Simulación de Consulta de Expediente Clínico Longitudinal

**Escenario clínico:** Un paciente con historial de 3 años regresa al hospital. El médico debe consultar su expediente completo: admisiones anteriores, notas, diagnósticos, tratamientos, signos vitales y valoraciones — todo en una sola consulta paginada.

**Entidades involucradas:** Todas las tablas SQL + colecciones MongoDB

**Acción:**
1. Token JWT rol `medico`.
2. `GET /pacientes/2/expediente?pagina=1&limite=20&orden=desc` — Expediente paginado.
3. Verificar que la respuesta incluye estructura anidada completa:
```json
{
  "paciente": { "id": 2, "nombre": "...", "curp": "..." },
  "notas_medicas": [...],
  "diagnosticos": [...],
  "tratamientos": [...],
  "signos_vitales": [...],
  "valoraciones": [...],
  "alertas_activas": [...],
  "total_registros": 47,
  "pagina_actual": 1
}
```
4. `GET /pacientes/2/timeline` → Vista cronológica de todos los eventos.
5. Verificar que el query SQL usa JOINs optimizados (< 3 queries totales).
6. Medir tiempo de respuesta total.

**Métricas esperadas:**
- Respuesta completa en < 500 ms para expediente de 47 registros.
- Estructura anidada correcta con todos los campos esperados.
- Paginación funcional: página 1 retorna 20 registros, página 2 los 27 restantes.

**Resultado esperado:** El sistema retorna el expediente clínico completo de forma coherente, paginada y optimizada, con datos de SQL y MongoDB integrados en una sola respuesta.

**Criterio de aprobación:**
- Tiempo de respuesta < 500 ms (P95).
- 0 registros huérfanos (diagnósticos sin nota, tratamientos sin diagnóstico).
- Paginación correcta sin duplicados.
- Datos MongoDB (alertas, valoraciones flexibles) incluidos en respuesta integrada.

---

### Prueba 8: Simulación de Demografía y Georeferenciación de Domicilios

**Escenario clínico:** El hospital necesita generar un reporte epidemiológico para identificar zonas geográficas con mayor incidencia de diagnósticos respiratorios (J00–J99 CIE-10), para planificar campañas de prevención.

**Entidades involucradas:** `md_pacientes`, `md_domicilios`, `md_personas_tiene_domicilio`, `md_diagnostico`

**Acción:**
1. Token JWT rol `admin`.
2. `GET /reportes/epidemiologia?codigo_cie_rango=J00-J99&estado=CDMX` — Reporte por estado.
3. Verificar que el sistema realiza JOIN entre pacientes → domicilios → diagnósticos:
```sql
SELECT d.municipio, d.colonia, COUNT(dx.id) as casos
FROM md_domicilios d
JOIN md_personas_tiene_domicilio ptd ON d.id = ptd.domicilio_id
JOIN md_pacientes p ON p.id = ptd.paciente_id
JOIN md_notas_medicas nm ON nm.paciente_id = p.id
JOIN md_diagnostico dx ON dx.nota_id = nm.id
WHERE dx.codigo_cie BETWEEN 'J00' AND 'J99'
GROUP BY d.municipio, d.colonia
ORDER BY casos DESC;
```
4. Respuesta debe retornar top 10 colonias con más casos respiratorios.
5. Verificar que el query se completa en < 1 segundo con dataset de prueba (500 pacientes).

**Métricas esperadas:**
- Reporte generado con datos correctos en < 1 segundo.
- Agrupación correcta por municipio y colonia.
- 0 duplicados en la agregación.

**Resultado esperado:** El sistema ejecuta análisis epidemiológico cruzando datos geográficos y diagnósticos clínicos, retornando resultados accionables para la toma de decisiones hospitalarias.

**Criterio de aprobación:**
- Tiempo de consulta < 1000 ms con 500 pacientes.
- Reporte con municipio, colonia, y conteo de casos ordenado correctamente.
- `codigo_cie_rango` inválido retorna HTTP 422.

---

### Prueba 9: Simulación de Seguridad, Roles JWT y Carga Concurrente de Sesiones

**Escenario clínico:** 20 usuarios (10 médicos + 10 administradores) se autentican simultáneamente. El sistema debe manejar la carga, respetar los permisos de rol, expirar tokens correctamente y registrar todas las sesiones en telemetría.

**Entidades involucradas:** `md_usuarios`, `telemetria_sesion` (MongoDB), `logs_auditoria`

**Escenarios de seguridad a probar:**

| Escenario | Endpoint | Rol requerido | Resultado esperado |
| :--- | :--- | :--- | :--- |
| Acceso sin token | `GET /pacientes` | Cualquiera | HTTP 401 Unauthorized |
| Token expirado | `POST /notas-medicas` | `medico` | HTTP 401 con msg `token_expirado` |
| Médico accede admin | `DELETE /usuarios/5` | `admin` | HTTP 403 Forbidden |
| Admin accede expediente | `GET /pacientes/1/expediente` | `medico` o `admin` | HTTP 200 OK |
| Token manipulado | Cualquier endpoint | N/A | HTTP 401 firma_invalida |

**Acción:**
1. Lanzar 20 requests de `POST /auth/login` simultáneos.
2. Para cada token obtenido, ejecutar request correspondiente a su rol.
3. Simular token expirado ajustando `exp` claim a fecha pasada.
4. Intentar acceso a rutas de admin con token de médico.
5. Verificar registro de cada sesión en `telemetria_sesion` MongoDB.
6. `GET /auditoria?accion=LOGIN&fecha=2026-05-21` → Verificar todos los eventos.

**Métricas esperadas:**
- 20/20 logins exitosos procesados en < 2 segundos totales.
- 100% de accesos no autorizados retornan HTTP 401 o 403.
- Cada login registrado en `telemetria_sesion` con: `usuario_id`, `ip`, `timestamp`, `rol`, `duracion_sesion`.

**Resultado esperado:** El sistema maneja concurrencia de autenticaciones correctamente, aplica guards de rol sin falsos positivos ni negativos, y persiste telemetría de sesión en MongoDB.

**Criterio de aprobación:**
- 0 accesos no autorizados con HTTP 200.
- 0 tokens de un rol que otorguen acceso a rutas del otro rol.
- Todos los logins registrados en `telemetria_sesion`.
- Tiempo de validación de JWT < 10 ms por request.

---

### Prueba 10: Simulación de Contingencia ante Fallo de Servicio e Integridad Transaccional

**Escenario clínico:** Durante la inserción de un expediente clínico completo (nota + diagnóstico + tratamiento en una sola transacción), se simula un fallo en la capa de persistencia a mitad de la transacción. El sistema debe garantizar rollback completo y no dejar datos parciales.

**Entidades involucradas:** `md_notas_medicas`, `md_diagnostico`, `md_tratamientos`, `logs_auditoria`

**Acción:**
1. Iniciar transacción SQL con nota médica + diagnóstico + tratamiento como unidad atómica.
2. Simular fallo en el tercer INSERT (tratamiento) — inyectar campo inválido.
3. Verificar rollback: `GET /notas-medicas?paciente_id=7` no debe mostrar la nota parcial.
4. Verificar en `logs_auditoria` MongoDB: evento `TRANSACTION_ROLLBACK` con detalles del fallo.
5. Repetir con escritura simultánea a MongoDB — verificar que el log de auditoría tampoco persiste si el rollback ocurre.

**Tabla de estados post-fallo esperados:**

| Tabla / Colección | Estado esperado tras rollback |
| :--- | :--- |
| `md_notas_medicas` | Sin registro nuevo |
| `md_diagnostico` | Sin registro nuevo |
| `md_tratamientos` | Sin registro nuevo |
| `logs_auditoria` | Registro de `TRANSACTION_ROLLBACK` presente |
| `valoraciones_flexibles` | Sin documento nuevo |

**Métricas esperadas:**
- Rollback completo en < 100 ms.
- 0 registros huérfanos en ninguna tabla SQL.
- Log de `TRANSACTION_ROLLBACK` en MongoDB con: `timestamp`, `tablas_afectadas`, `motivo_fallo`, `rollback_exitoso: true`.

**Resultado esperado:** El sistema garantiza atomicidad completa en operaciones multi-tabla mediante transacciones SQLAlchemy, y registra todos los fallos en MongoDB para auditoría posterior.

**Criterio de aprobación:**
- 100% de transacciones fallidas resultan en rollback completo (sin datos huérfanos).
- Log de rollback siempre presente en `logs_auditoria`.
- Sistema se recupera automáticamente y acepta nuevas transacciones tras el fallo.

---

## 7. Registro de Resultados

Completar la siguiente tabla para cada ejecución de pruebas:

| ID | Nombre de Prueba | Fecha | Ejecutado por | Resultado Esperado | Resultado Real | Estado | Observaciones |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PRB-01 | Registro Masivo de Pacientes | | | 13 OK, 2 Rechazados | | ⬜ | |
| PRB-02 | Triage y Signos Vitales | | | 4 Alertas Críticas | | ⬜ | |
| PRB-03 | Nota Clínica y Diagnóstico CIE-10 | | | Cadena íntegra | | ⬜ | |
| PRB-04 | Interacciones Farmacológicas | | | HTTP 409 + Advertencia | | ⬜ | |
| PRB-05 | Alertas por Signos Críticos | | | CODIGO_AZUL < 200ms | | ⬜ | |
| PRB-06 | Escalas de Valoración (Glasgow) | | | Clasificación correcta | | ⬜ | |
| PRB-07 | Expediente Longitudinal | | | < 500ms, paginado | | ⬜ | |
| PRB-08 | Demografía y Epidemiología | | | Top 10 colonias | | ⬜ | |
| PRB-09 | Seguridad y Roles JWT | | | 0 accesos no autorizados | | ⬜ | |
| PRB-10 | Integridad Transaccional | | | Rollback completo | | ⬜ | |

---

## 8. Conclusiones y Seguimiento

- Asegurar la resolución de todas las deficiencias encontradas antes del siguiente sprint.
- Repetir las pruebas PRB-02, PRB-05 y PRB-09 después de cada cambio en el motor de decisión clínica.
- Actualizar los umbrales de alertas (Prueba 5) si el equipo médico modifica los rangos de referencia.
- Coordinar con el equipo de QA (Artiaga Morales) para automatizar las pruebas PRB-07 y PRB-10 mediante pytest.

---

## 9. Anexos

- **Anexo A:** Scripts de seed: `Deliverables/API/source/seed_db.py`
- **Anexo B:** Colección Postman para todos los endpoints: `Deliverables/API/source/Quantify_API.postman_collection.json`
- **Anexo C:** Diccionario de datos SQL: `DataBases/SQL/DD/README.md`
- **Anexo D:** Esquemas NoSQL: `DataBases/NoSQL/Schemas/README.md`
- **Anexo E:** Catálogo CIE-10 simplificado (códigos J00–J99, I00–I99, K00–K99)

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Completado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | En revisión |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En revisión |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En revisión |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |
