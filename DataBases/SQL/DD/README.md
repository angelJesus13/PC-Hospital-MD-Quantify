# DD — Diccionario de Datos SQL

> **Proyecto:** PC-Hospital-MD-Quantify  
> **Motor:** MySQL 8.0+  
> **API de referencia:** [MEDICAL_REGISTER_API](https://github.com/AngelJdev/MEDICAL_REGISTER_API)  
> **Versión:** 2.0.0

---

## 1. Descripción General

El **Diccionario de Datos (DD)** documenta de forma exhaustiva cada tabla, columna, tipo de dato, restricción y regla de negocio del subsistema SQL de `PC-Hospital-MD-Quantify`. Es la fuente de verdad para desarrolladores, analistas y DBAs.

---

## 2. Tabla: `md_usuarios`

**Propósito:** Gestionar los usuarios del sistema clínico con autenticación JWT y control de acceso por roles.

| Campo | Tipo | Nulo | PK/FK | Único | Defecto | Descripción |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `id` | INT UNSIGNED | ❌ | PK | ✅ | AUTO_INCREMENT | Identificador único del usuario |
| `username` | VARCHAR(80) | ❌ | — | ✅ | — | Nombre de usuario para login. Alfanumérico, sin espacios |
| `email` | VARCHAR(120) | ❌ | — | ✅ | — | Correo institucional. Validado con formato RFC 5322 |
| `password_hash` | VARCHAR(200) | ❌ | — | ❌ | — | Hash bcrypt de la contraseña. Factor de costo=12 |
| `role` | ENUM | ❌ | — | ❌ | `medico` | Rol del usuario: `admin`, `medico`, `enfermero` |
| `activo` | BOOLEAN | ❌ | — | ❌ | `TRUE` | Soft delete. `FALSE` = cuenta desactivada sin borrar |
| `created_at` | DATETIME | ❌ | — | ❌ | `NOW()` | Timestamp de creación (UTC) |
| `updated_at` | DATETIME | ✅ | — | ❌ | `NULL` | Timestamp de última modificación. Auto-actualizado |

**Valores ENUM `role`:**
- `admin` — Acceso total al sistema, gestión de usuarios y reportes
- `medico` — Acceso clínico completo (notas, diagnósticos, tratamientos)
- `enfermero` — Registro de signos vitales y consulta de expedientes (solo lectura en notas)

---

## 3. Tabla: `md_pacientes`

**Propósito:** Registro maestro de pacientes. Entidad central del sistema clínico.

| Campo | Tipo | Nulo | PK/FK | Único | Defecto | Descripción |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `id` | INT UNSIGNED | ❌ | PK | ✅ | AUTO_INCREMENT | Identificador único del paciente |
| `nombre` | VARCHAR(100) | ❌ | — | ❌ | — | Nombre completo. Formato: Apellido1 Apellido2 Nombre(s) |
| `curp` | CHAR(18) | ❌ | — | ✅ | — | CURP oficial mexicana. Patrón: `[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d` |
| `fecha_nacimiento` | DATE | ✅ | — | ❌ | `NULL` | Fecha de nacimiento. Formato: YYYY-MM-DD |
| `sexo` | ENUM | ✅ | — | ❌ | `NULL` | `M`=Masculino, `F`=Femenino, `NB`=No binario |
| `telefono` | VARCHAR(15) | ✅ | — | ❌ | `NULL` | Teléfono de contacto (formato internacional +52) |
| `fecha_registro` | DATETIME | ❌ | — | ❌ | — | Fecha y hora de primer registro en el hospital |
| `created_at` | DATETIME | ❌ | — | ❌ | `NOW()` | Timestamp de creación del registro |

**Reglas de negocio:**
- La CURP debe ser única en todo el sistema. Un intento de duplicado retorna HTTP 409.
- Un paciente no puede eliminarse si tiene notas médicas, nacimientos o defunciones asociadas.

---

## 4. Tabla: `md_notas_medicas`

**Propósito:** Registro cronológico de episodios clínicos documentados por los médicos.

| Campo | Tipo | Nulo | PK/FK | Único | Defecto | Descripción |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `id` | INT UNSIGNED | ❌ | PK | ✅ | AUTO_INCREMENT | Identificador único de la nota |
| `paciente_id` | INT UNSIGNED | ❌ | FK→`md_pacientes.id` | ❌ | — | Referencia al paciente. CASCADE al eliminar paciente |
| `medico_id` | INT UNSIGNED | ❌ | FK→`md_usuarios.id` | ❌ | — | Médico autor. RESTRICT al eliminar usuario |
| `contenido` | TEXT | ❌ | — | ❌ | — | Texto clínico libre de la nota médica. Sin límite de caracteres |
| `tipo_nota` | ENUM | ❌ | — | ❌ | — | Tipo de nota clínica (ver valores abajo) |
| `fecha` | DATETIME | ❌ | — | ❌ | — | Fecha y hora de redacción de la nota |
| `created_at` | DATETIME | ❌ | — | ❌ | `NOW()` | Timestamp de inserción en BD |

**Valores ENUM `tipo_nota`:**
- `ingreso` — Primera evaluación clínica al admitir al paciente
- `evolucion` — Seguimiento diario o de turno de la condición
- `egreso` — Resumen al dar de alta al paciente
- `interconsulta` — Nota de especialista consultado por otro médico
- `urgencias` — Atención en servicio de urgencias

---

## 5. Tabla: `md_signos_vitales`

**Propósito:** Registro de parámetros fisiológicos para monitoreo continuo y cálculo de scores de riesgo (MEWS).

| Campo | Tipo | Nulo | PK/FK | Rango válido | Unidad | Descripción |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id` | INT UNSIGNED | ❌ | PK | — | — | Identificador único |
| `paciente_id` | INT UNSIGNED | ❌ | FK→`md_pacientes.id` | — | — | Paciente al que pertenece el registro |
| `tension_arterial` | VARCHAR(20) | ✅ | — | — | mmHg | Formato `sistólica/diastólica`. Ej: `120/80` |
| `frecuencia_cardiaca` | INT UNSIGNED | ✅ | — | 0–300 | lpm | Latidos por minuto |
| `temperatura` | DECIMAL(5,2) | ✅ | — | 30.0–45.0 | °C | Temperatura corporal en Celsius |
| `frecuencia_respiratoria` | INT UNSIGNED | ✅ | — | 0–60 | rpm | Respiraciones por minuto |
| `saturacion_o2` | INT UNSIGNED | ✅ | — | 0–100 | % | Saturación de oxígeno en sangre (SpO2) |
| `escala_consciencia` | VARCHAR(30) | ✅ | — | — | — | Nivel de consciencia: alerta, confuso, somnoliento, inconsciente |
| `score_mews` | INT UNSIGNED | ❌ | — | 0–14 | pts | Score MEWS calculado automáticamente |
| `fecha` | DATETIME | ❌ | — | — | — | Fecha y hora de la toma de signos |

**Cálculo automático `score_mews`:**

| Parámetro | Puntos críticos |
| :--- | :--- |
| FC < 40 o > 130 | +2 pts |
| FR > 25 | +2 pts |
| SpO2 < 90% | +3 pts |
| Temperatura > 38.5 | +1 pt |
| Nivel de consciencia alterado | +1–3 pts |

Score ≥ 5 → Alerta crítica automática en MongoDB `valoraciones_flexibles`.

---

## 6. Tabla: `md_diagnostico`

**Propósito:** Diagnósticos médicos formales vinculados a notas clínicas, con codificación CIE-10.

| Campo | Tipo | Nulo | PK/FK | Único | Defecto | Descripción |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `id` | INT UNSIGNED | ❌ | PK | ✅ | AUTO_INCREMENT | Identificador único |
| `nota_id` | INT UNSIGNED | ❌ | FK→`md_notas_medicas.id` | ❌ | — | Nota médica a la que pertenece el diagnóstico. CASCADE |
| `descripcion` | TEXT | ❌ | — | ❌ | — | Descripción clínica detallada del diagnóstico |
| `codigo_cie` | CHAR(7) | ✅ | — | ❌ | `NULL` | Código CIE-10. Patrón: `^[A-Z][0-9]{2}(\.[0-9]{1,2})?$` |
| `severidad` | ENUM | ❌ | — | ❌ | `leve` | Gravedad: `leve`, `moderado`, `grave`, `critico` |
| `activo` | BOOLEAN | ❌ | — | ❌ | `TRUE` | Soft delete. `FALSE` = diagnóstico resuelto o descartado |

**Ejemplos de códigos CIE-10:**
- `J18.9` — Neumonía no especificada
- `I10` — Hipertensión esencial
- `E11.9` — Diabetes mellitus tipo 2 sin complicaciones
- `K29.7` — Gastritis no especificada
- `S06.0` — Conmoción cerebral (TEC)

---

## 7. Tabla: `md_tratamientos`

**Propósito:** Prescripciones médicas asociadas a un diagnóstico específico.

| Campo | Tipo | Nulo | PK/FK | Defecto | Descripción |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `id` | INT UNSIGNED | ❌ | PK | AUTO_INCREMENT | Identificador único |
| `diagnostico_id` | INT UNSIGNED | ❌ | FK→`md_diagnostico.id` | — | Diagnóstico que origina la prescripción. CASCADE |
| `medicamento` | VARCHAR(200) | ❌ | — | — | Nombre completo del medicamento (DCI preferido) |
| `dosis` | VARCHAR(50) | ❌ | — | — | Dosis por toma. Ej: `500 mg`, `10 UI` |
| `frecuencia` | VARCHAR(50) | ❌ | — | — | Intervalo entre dosis. Ej: `cada 8 horas`, `dos veces al día` |
| `duracion` | VARCHAR(30) | ❌ | — | — | Duración del tratamiento. Ej: `7 días`, `hasta nuevo aviso` |
| `activo` | BOOLEAN | ❌ | — | `TRUE` | `FALSE` = tratamiento concluido o suspendido |
| `fecha_inicio` | DATETIME | ✅ | — | `NULL` | Inicio del tratamiento |
| `fecha_fin` | DATETIME | ✅ | — | `NULL` | Calculado como `fecha_inicio + duracion` |

---

## 8. Tabla: `md_nacimientos`

**Propósito:** Datos del nacimiento de un paciente (relación 1:1 con `md_pacientes`).

| Campo | Tipo | Nulo | PK/FK | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT UNSIGNED | ❌ | PK | Identificador único |
| `paciente_id` | INT UNSIGNED | ❌ | FK UNIQUE | Paciente. RESTRICT al eliminar. Un paciente → un nacimiento |
| `fecha_nacimiento` | DATE | ❌ | — | Fecha de nacimiento (YYYY-MM-DD) |
| `lugar` | VARCHAR(200) | ❌ | — | Hospital, ciudad o estado de nacimiento |
| `nombre_madre` | VARCHAR(100) | ✅ | — | Nombre completo de la madre |
| `nombre_padre` | VARCHAR(100) | ✅ | — | Nombre completo del padre |
| `peso_al_nacer` | DECIMAL(5,2) | ✅ | — | Peso en kg. Ej: `3.25` |
| `talla_al_nacer` | DECIMAL(5,2) | ✅ | — | Talla en cm. Ej: `50.00` |

---

## 9. Tabla: `md_defunciones`

**Propósito:** Registro de defunciones hospitalarias (relación 1:0..1 con `md_pacientes`).

| Campo | Tipo | Nulo | PK/FK | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT UNSIGNED | ❌ | PK | Identificador único |
| `paciente_id` | INT UNSIGNED | ❌ | FK UNIQUE | Paciente fallecido. RESTRICT al eliminar |
| `fecha_defuncion` | DATETIME | ❌ | — | Fecha y hora del deceso (UTC) |
| `causa` | TEXT | ❌ | — | Causa inmediata de muerte (ej: insuficiencia cardíaca aguda) |
| `causa_basica` | TEXT | ✅ | — | Enfermedad o condición subyacente que originó la causa inmediata |
| `certificador` | VARCHAR(50) | ✅ | — | Nombre del médico que certifica la defunción |

---

## 10. Tabla: `md_documentos_oficiales`

**Propósito:** Documentos de identidad y derechohabiencia vinculados a un paciente.

| Campo | Tipo | Nulo | PK/FK | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT UNSIGNED | ❌ | PK | Identificador único |
| `paciente_id` | INT UNSIGNED | ❌ | FK→`md_pacientes.id` | Paciente propietario del documento. CASCADE |
| `tipo_documento` | ENUM | ❌ | — | `ine`, `curp`, `nss`, `pasaporte`, `acta_nacimiento` |
| `numero_documento` | VARCHAR(60) | ❌ | — | Número o folio único del documento |
| `fecha_emision` | DATE | ✅ | — | Fecha de emisión del documento |
| `fecha_vencimiento` | DATE | ✅ | — | Fecha de vencimiento (si aplica) |
| `vigente` | BOOLEAN | ❌ | — | `TRUE` = documento válido y vigente |

---

## 11. Tabla: `md_domicilios`

**Propósito:** Catálogo de domicilios con coordenadas GPS para análisis epidemiológico geoespacial.

| Campo | Tipo | Nulo | PK/FK | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT UNSIGNED | ❌ | PK | Identificador único |
| `calle` | VARCHAR(200) | ❌ | — | Nombre de calle y número exterior/interior |
| `colonia` | VARCHAR(100) | ❌ | — | Colonia o fraccionamiento |
| `municipio` | VARCHAR(100) | ❌ | — | Municipio o alcaldía |
| `estado` | VARCHAR(60) | ❌ | — | Estado de la República Mexicana |
| `cp` | CHAR(5) | ❌ | — | Código Postal de 5 dígitos |
| `latitud` | DECIMAL(10,7) | ✅ | — | Latitud GPS. Rango: -90.0 a 90.0 |
| `longitud` | DECIMAL(10,7) | ✅ | — | Longitud GPS. Rango: -180.0 a 180.0 |

---

## 12. Tabla: `md_personas_tiene_domicilio`

**Propósito:** Tabla intermedia para la relación N:M entre pacientes y domicilios.

| Campo | Tipo | Nulo | PK/FK | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT UNSIGNED | ❌ | PK | Identificador único |
| `paciente_id` | INT UNSIGNED | ❌ | FK→`md_pacientes.id` | Paciente. CASCADE |
| `domicilio_id` | INT UNSIGNED | ❌ | FK→`md_domicilios.id` | Domicilio. CASCADE |
| `tipo_domicilio` | ENUM | ❌ | — | `principal`, `temporal`, `referencia` |
| `activo` | BOOLEAN | ❌ | — | `TRUE` = vinculación activa |

**Restricción única:** `(paciente_id, domicilio_id, tipo_domicilio)` — Un paciente no puede tener dos domicilios del mismo tipo activos simultáneamente.

---

## 13. Tabla: `md_valoraciones`

**Propósito:** Registro de resultados de escalas clínicas estandarizadas (resumen SQL; detalle en MongoDB).

| Campo | Tipo | Nulo | PK/FK | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | INT UNSIGNED | ❌ | PK | Identificador único |
| `paciente_id` | INT UNSIGNED | ❌ | FK→`md_pacientes.id` | Paciente evaluado. CASCADE |
| `escala` | VARCHAR(50) | ❌ | — | Nombre de la escala: `Glasgow`, `MEWS`, `APGAR`, `Braden`, `Norton`, `SOFA` |
| `resultado` | VARCHAR(10) | ✅ | — | Puntaje total o clasificación (ej: `8`, `GRAVE`, `7/10`) |
| `observaciones` | TEXT | ✅ | — | Notas adicionales del evaluador |
| `fecha` | DATETIME | ❌ | — | Fecha y hora de la valoración |
| `registrado_por` | INT UNSIGNED | ✅ | FK→`md_usuarios.id` | Usuario que registró la valoración. SET NULL si se elimina |

**Escalas y rangos de interpretación:**

| Escala | Rango | Interpretación |
| :--- | :--- | :--- |
| Glasgow | 3–15 | ≤8=Grave, 9–12=Moderado, 13–15=Leve |
| MEWS | 0–14 | 0–4=Bajo, 5–6=Medio, ≥7=Alto |
| APGAR | 0–10 | ≤3=Crítico, 4–6=Regular, 7–10=Normal |
| Braden | 6–23 | ≤9=Muy alto riesgo, 10–12=Alto, 13–14=Moderado |

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |  Revisado y Aprobado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En Revision |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En Revision |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |