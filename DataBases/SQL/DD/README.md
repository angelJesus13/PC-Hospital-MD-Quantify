# Diccionario de Datos SQL

> **Proyecto:** PC-Hospital-MD-Quantify  
> **Motor:** MySQL 8.0+  
> **API de referencia:** [MEDICAL_REGISTER_API](https://github.com/AngelJdev/MEDICAL_REGISTER_API)  
> **Version:** 2.0.0

## 1. Proposito

Este documento describe la persistencia relacional utilizada por
`PC-Hospital-MD-Quantify`. Su objetivo es identificar con precision las tablas,
columnas, tipos de datos, restricciones, relaciones e indices que aparecen en
el repositorio.

La solucion contiene dos esquemas SQL con responsabilidades distintas:

| Esquema | Base de datos por defecto | Uso | Fuente principal |
| --- | --- | --- | --- |
| API clinica principal | `quantify_medical_db` | Persistencia transaccional consumida por la API hibrida | `Deliverables/API/source/init_db.sql` |
| Pruebas de volumen | `hospital_hibrido_md` | Simulacion masiva de notas medicas y auditoria | `Deliverables/API/source/volume_tests/config/db_mysql.py` |

Las tablas de pruebas de volumen no sustituyen a las tablas `md_*` de la API.
Se documentan por separado porque ambas familias se usan dentro del
repositorio.

## 2. Convenciones

| Marca | Significado |
| --- | --- |
| PK | Llave primaria |
| FK | Llave foranea |
| UK | Restriccion o indice unico |
| NN | `NOT NULL` |
| AI | `AUTO_INCREMENT` |
| `CASCADE` | El cambio o eliminacion se propaga al registro dependiente |
| `RESTRICT` | La eliminacion se rechaza si existen registros dependientes |
| `SET NULL` | La referencia se conserva como `NULL` al eliminar el registro padre |

Todas las tablas del esquema principal usan `InnoDB`, `utf8mb4` y
`utf8mb4_unicode_ci`. En MySQL, `BOOLEAN` se almacena como un alias de
`TINYINT(1)`.

## 3. Resumen del Esquema Principal

| Tabla | Proposito |
| --- | --- |
| `md_usuarios` | Usuarios autenticables y roles de acceso |
| `md_pacientes` | Registro maestro de pacientes |
| `md_notas_medicas` | Historial cronologico de notas clinicas |
| `md_signos_vitales` | Tomas fisiologicas y puntaje MEWS |
| `md_diagnostico` | Diagnosticos asociados con notas medicas |
| `md_tratamientos` | Prescripciones asociadas con diagnosticos |
| `md_nacimientos` | Informacion de nacimiento del paciente |
| `md_defunciones` | Registro opcional de defuncion |
| `md_documentos_oficiales` | Documentos de identidad del paciente |
| `md_domicilios` | Catalogo de domicilios georreferenciables |
| `md_personas_tiene_domicilio` | Relacion N:M entre pacientes y domicilios |
| `md_valoraciones` | Resumen SQL de escalas clinicas |

## 4. Tablas del Esquema Principal

### 4.1 `md_usuarios`

Usuarios del sistema clinico. La autenticacion consulta `username`,
`password_hash` y `activo`; la autorizacion utiliza `role`.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador interno |
| `username` | `VARCHAR(80)` | No | UK `idx_usuarios_username` | - | Nombre unico para iniciar sesion |
| `email` | `VARCHAR(120)` | No | UK `idx_usuarios_email` | - | Correo unico del usuario |
| `password_hash` | `VARCHAR(200)` | No | - | - | Hash bcrypt de la contrasena |
| `role` | `ENUM('admin','medico','enfermero')` | No | INDEX `idx_usuarios_role` | `'medico'` | Rol de autorizacion |
| `activo` | `BOOLEAN` | No | - | `TRUE` | Indica si la cuenta puede autenticarse |
| `created_at` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Fecha de creacion |
| `updated_at` | `DATETIME` | Si | Actualizado al modificar el registro | `NULL` | Ultima modificacion |

### 4.2 `md_pacientes`

Entidad central del expediente clinico. La API valida la CURP con el patron
oficial mexicano de 18 caracteres antes de insertar el registro.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador interno |
| `nombre` | `VARCHAR(100)` | No | INDEX `idx_pacientes_nombre` | - | Nombre completo |
| `curp` | `CHAR(18)` | No | UK `idx_pacientes_curp` | - | CURP unica |
| `fecha_nacimiento` | `DATE` | Si | - | `NULL` | Fecha de nacimiento |
| `sexo` | `ENUM('M','F','NB')` | Si | - | `NULL` | Sexo registrado |
| `telefono` | `VARCHAR(15)` | Si | - | `NULL` | Telefono de contacto |
| `fecha_registro` | `DATETIME` | No | INDEX `idx_pacientes_fecha_registro` | - | Fecha de alta hospitalaria |
| `created_at` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Fecha de insercion |

### 4.3 `md_notas_medicas`

Notas del historial clinico. Cada registro pertenece a un paciente y conserva
el usuario medico que lo redacto.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador de la nota |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id` | - | Paciente propietario |
| `medico_id` | `INT UNSIGNED` | No | FK a `md_usuarios.id` | - | Usuario medico autor |
| `contenido` | `TEXT` | No | - | - | Texto clinico |
| `tipo_nota` | `ENUM('ingreso','evolucion','egreso','interconsulta','urgencias')` | No | INDEX `idx_notas_tipo` | - | Clasificacion de la nota |
| `fecha` | `DATETIME` | No | INDEX compuesto con `paciente_id` | - | Fecha clinica |
| `created_at` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Fecha de insercion |

**Indices:** `idx_notas_paciente_fecha(paciente_id, fecha)` e
`idx_notas_medico(medico_id)`.

**Integridad referencial:** al eliminar un paciente se eliminan sus notas
(`CASCADE`). Un usuario medico con notas asociadas no puede eliminarse
(`RESTRICT`). Ambas FK propagan actualizaciones de identificador (`ON UPDATE
CASCADE`).

### 4.4 `md_signos_vitales`

Tomas fisiologicas asociadas con pacientes. La API calcula `score_mews` antes
de persistir cada toma.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador de la toma |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id` | - | Paciente monitoreado |
| `tension_arterial` | `VARCHAR(20)` | Si | API: patron `sistolica/diastolica` | `NULL` | Presion arterial en mmHg |
| `frecuencia_cardiaca` | `INT UNSIGNED` | Si | CHECK `0..300` | `NULL` | Latidos por minuto |
| `temperatura` | `DECIMAL(5,2)` | Si | CHECK `30.0..45.0` | `NULL` | Temperatura en grados Celsius |
| `frecuencia_respiratoria` | `INT UNSIGNED` | Si | CHECK `0..60` | `NULL` | Respiraciones por minuto |
| `saturacion_o2` | `INT UNSIGNED` | Si | CHECK `0..100` | `NULL` | Saturacion de oxigeno en porcentaje |
| `escala_consciencia` | `VARCHAR(30)` | Si | - | `NULL` | Descripcion del estado de consciencia |
| `score_mews` | `INT UNSIGNED` | No | INDEX `idx_sv_score_mews` | `0` | Puntaje calculado por la API |
| `fecha` | `DATETIME` | No | INDEX compuesto con `paciente_id` | - | Fecha de la toma |

**Indice:** `idx_sv_paciente_fecha(paciente_id, fecha DESC)`.

**Integridad referencial:** `paciente_id` usa eliminacion `CASCADE`.

**Regla de aplicacion:** `utils/helpers.py` calcula el MEWS usando frecuencia
cardiaca, frecuencia respiratoria, saturacion de oxigeno, temperatura y
consciencia. Cuando el resultado es mayor o igual a `5`, la ruta de signos
vitales registra una alerta en MongoDB. El valor no se calcula mediante un
trigger SQL.

### 4.5 `md_diagnostico`

Diagnosticos medicos asociados con una nota clinica.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del diagnostico |
| `nota_id` | `INT UNSIGNED` | No | FK a `md_notas_medicas.id` | - | Nota que origina el diagnostico |
| `descripcion` | `TEXT` | No | - | - | Descripcion clinica |
| `codigo_cie` | `CHAR(7)` | Si | INDEX `idx_dx_codigo_cie` | `NULL` | Codigo CIE-10 |
| `severidad` | `ENUM('leve','moderado','grave','critico')` | No | INDEX `idx_dx_severidad` | `'leve'` | Nivel de gravedad |
| `activo` | `BOOLEAN` | No | - | `TRUE` | Estado vigente del diagnostico |

**Indice:** `idx_dx_nota(nota_id)`.

**Integridad referencial:** `nota_id` usa eliminacion `CASCADE`.

**Regla de aplicacion:** el esquema Pydantic valida `codigo_cie` con el patron
`^[A-Z][0-9]{2}(\.[0-9]{1,2})?$`.

### 4.6 `md_tratamientos`

Prescripciones vinculadas con un diagnostico.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del tratamiento |
| `diagnostico_id` | `INT UNSIGNED` | No | FK a `md_diagnostico.id` | - | Diagnostico relacionado |
| `medicamento` | `VARCHAR(200)` | No | INDEX `idx_tx_medicamento` | - | Nombre del medicamento |
| `dosis` | `VARCHAR(50)` | No | - | - | Dosis indicada |
| `frecuencia` | `VARCHAR(50)` | No | - | - | Periodicidad |
| `duracion` | `VARCHAR(30)` | No | - | - | Duracion expresada como texto |
| `activo` | `BOOLEAN` | No | INDEX `idx_tx_activo` | `TRUE` | Estado del tratamiento |
| `fecha_inicio` | `DATETIME` | Si | - | `NULL` | Inicio opcional |
| `fecha_fin` | `DATETIME` | Si | - | `NULL` | Fin opcional |

**Indice:** `idx_tx_diagnostico(diagnostico_id)`.

**Integridad referencial:** `diagnostico_id` usa eliminacion `CASCADE`.

### 4.7 `md_nacimientos`

Registro opcional y unico de nacimiento para un paciente.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del registro |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id`, UK `idx_nac_paciente` | - | Paciente relacionado |
| `fecha_nacimiento` | `DATE` | No | - | - | Fecha de nacimiento |
| `lugar` | `VARCHAR(200)` | No | - | - | Lugar de nacimiento |
| `nombre_madre` | `VARCHAR(100)` | Si | - | `NULL` | Nombre de la madre |
| `nombre_padre` | `VARCHAR(100)` | Si | - | `NULL` | Nombre del padre |
| `peso_al_nacer` | `DECIMAL(5,2)` | Si | - | `NULL` | Peso en kilogramos |
| `talla_al_nacer` | `DECIMAL(5,2)` | Si | - | `NULL` | Talla en centimetros |

**Integridad referencial:** `paciente_id` usa eliminacion `RESTRICT`.

### 4.8 `md_defunciones`

Registro opcional y unico de defuncion para un paciente.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del registro |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id`, UK `idx_def_paciente` | - | Paciente relacionado |
| `fecha_defuncion` | `DATETIME` | No | INDEX `idx_def_fecha` | - | Fecha y hora de defuncion |
| `causa` | `TEXT` | No | - | - | Causa inmediata |
| `causa_basica` | `TEXT` | Si | - | `NULL` | Causa subyacente |
| `certificador` | `VARCHAR(50)` | Si | - | `NULL` | Nombre del certificador |

**Integridad referencial:** `paciente_id` usa eliminacion `RESTRICT`.

### 4.9 `md_documentos_oficiales`

Documentos de identidad vinculados con pacientes.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del documento |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id` | - | Paciente propietario |
| `tipo_documento` | `ENUM('ine','curp','nss','pasaporte','acta_nacimiento')` | No | INDEX `idx_docs_tipo` | - | Tipo de documento |
| `numero_documento` | `VARCHAR(60)` | No | UK compuesto con `tipo_documento` | - | Folio o numero |
| `fecha_emision` | `DATE` | Si | - | `NULL` | Fecha de emision |
| `fecha_vencimiento` | `DATE` | Si | - | `NULL` | Fecha de vencimiento |
| `vigente` | `BOOLEAN` | No | - | `TRUE` | Vigencia declarada |

**Indices:** `idx_docs_paciente(paciente_id)` e
`idx_docs_numero(tipo_documento, numero_documento)`.

**Integridad referencial:** `paciente_id` usa eliminacion `CASCADE`.

### 4.10 `md_domicilios`

Catalogo de domicilios con coordenadas opcionales.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del domicilio |
| `calle` | `VARCHAR(200)` | No | - | - | Calle y numero |
| `colonia` | `VARCHAR(100)` | No | - | - | Colonia |
| `municipio` | `VARCHAR(100)` | No | INDEX `idx_dom_municipio` | - | Municipio o alcaldia |
| `estado` | `VARCHAR(60)` | No | INDEX `idx_dom_estado` | - | Entidad federativa |
| `cp` | `CHAR(5)` | No | INDEX `idx_dom_cp` | - | Codigo postal |
| `latitud` | `DECIMAL(10,7)` | Si | API: rango `-90..90` | `NULL` | Coordenada geografica |
| `longitud` | `DECIMAL(10,7)` | Si | API: rango `-180..180` | `NULL` | Coordenada geografica |

### 4.11 `md_personas_tiene_domicilio`

Tabla intermedia que implementa la relacion N:M entre pacientes y domicilios.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador del vinculo |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id` | - | Paciente |
| `domicilio_id` | `INT UNSIGNED` | No | FK a `md_domicilios.id` | - | Domicilio |
| `tipo_domicilio` | `ENUM('principal','temporal','referencia')` | No | UK compuesto | `'principal'` | Clasificacion del vinculo |
| `activo` | `BOOLEAN` | No | - | `TRUE` | Estado del vinculo |

**Indices:** `idx_ptd_unique(paciente_id, domicilio_id, tipo_domicilio)`,
`idx_ptd_paciente(paciente_id)` e `idx_ptd_domicilio(domicilio_id)`.

**Integridad referencial:** ambas FK usan eliminacion `CASCADE`.

### 4.12 `md_valoraciones`

Resumen relacional de escalas clinicas. Los componentes flexibles se guardan
en la coleccion MongoDB `valoraciones_flexibles`.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `id` | `INT UNSIGNED` | No | PK, AI | - | Identificador de la valoracion |
| `paciente_id` | `INT UNSIGNED` | No | FK a `md_pacientes.id` | - | Paciente evaluado |
| `escala` | `VARCHAR(50)` | No | CHECK de catalogo | - | Nombre de la escala |
| `resultado` | `VARCHAR(10)` | Si | - | `NULL` | Puntaje o clasificacion |
| `observaciones` | `TEXT` | Si | - | `NULL` | Comentarios |
| `fecha` | `DATETIME` | No | INDEX compuesto con `paciente_id` | - | Fecha de valoracion |
| `registrado_por` | `INT UNSIGNED` | Si | FK a `md_usuarios.id` | `NULL` | Usuario que registro la escala |

**Catalogo de escalas:** `Glasgow`, `MEWS`, `APGAR`, `Braden`, `Norton` y
`SOFA`.

**Indices:** `idx_val_paciente_fecha(paciente_id, fecha DESC)` e
`idx_val_escala(escala)`.

**Integridad referencial:** `paciente_id` usa eliminacion `CASCADE` y
`registrado_por` usa `SET NULL`.

## 5. Relaciones del Esquema Principal

| Tabla origen | Cardinalidad | Tabla destino | Llave foranea | Eliminacion |
| --- | --- | --- | --- | --- |
| `md_usuarios` | 1:N | `md_notas_medicas` | `medico_id` | `RESTRICT` |
| `md_usuarios` | 1:N | `md_valoraciones` | `registrado_por` | `SET NULL` |
| `md_pacientes` | 1:N | `md_notas_medicas` | `paciente_id` | `CASCADE` |
| `md_pacientes` | 1:N | `md_signos_vitales` | `paciente_id` | `CASCADE` |
| `md_pacientes` | 1:N | `md_documentos_oficiales` | `paciente_id` | `CASCADE` |
| `md_pacientes` | 1:N | `md_valoraciones` | `paciente_id` | `CASCADE` |
| `md_pacientes` | 1:0..1 | `md_nacimientos` | `paciente_id` | `RESTRICT` |
| `md_pacientes` | 1:0..1 | `md_defunciones` | `paciente_id` | `RESTRICT` |
| `md_pacientes` | N:M | `md_domicilios` | Via `md_personas_tiene_domicilio` | `CASCADE` |
| `md_notas_medicas` | 1:N | `md_diagnostico` | `nota_id` | `CASCADE` |
| `md_diagnostico` | 1:N | `md_tratamientos` | `diagnostico_id` | `CASCADE` |

## 6. Tablas para Pruebas de Volumen

Estas tablas son creadas por
`Deliverables/API/source/volume_tests/config/db_mysql.py`. Su base de datos por
defecto es `hospital_hibrido_md`, configurable mediante `MYSQL_DB`.

### 6.1 `tbb_md_pacientes`

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `ID` | `INT UNSIGNED` | No | PK, AI | - | Identificador |
| `status_medico` | `VARCHAR(150)` | Si | - | `NULL` | Resumen clinico |
| `status_vida` | `ENUM('Vivo','Finado','Coma','Vegetativo','Desconocido')` | No | - | `'Desconocido'` | Estado vital |
| `fecha_ultima_citamedica` | `DATETIME` | Si | - | `NULL` | Ultima cita |
| `fecha_registro` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Alta |
| `fecha_actualizacion` | `DATETIME` | Si | - | `NULL` | Modificacion |
| `estatus` | `BIT(1)` | No | - | `b'1'` | Estado logico |

### 6.2 `tbb_hr_personal_medico`

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `ID` | `INT UNSIGNED` | No | PK, AI | - | Identificador |
| `Turno` | `ENUM('MATUTINO','VESPERTINO','NOCTURNO A','NOCTURNO B','JORNADA ACUMULADA')` | Si | - | `NULL` | Turno laboral |
| `Area_ID` | `INT UNSIGNED` | No | Referencia simulada sin FK | - | Area clinica |
| `Fecha_Registro` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Alta |
| `Fecha_Actualizacion` | `DATETIME` | Si | - | `NULL` | Modificacion |
| `Estatus` | `BIT(1)` | No | - | `b'1'` | Estado logico |
| `Cedula_Profesional` | `VARCHAR(30)` | No | UK | - | Cedula profesional |
| `Especialidad` | `VARCHAR(100)` | No | - | - | Especialidad |

### 6.3 `tbb_md_expedientes_medicos`

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `ID` | `INT UNSIGNED` | No | PK, AI | - | Identificador |
| `numero_expediente` | `VARCHAR(50)` | No | UK | - | Folio del expediente |
| `Paciente_ID` | `INT UNSIGNED` | No | FK a `tbb_md_pacientes.ID`, UK | - | Paciente |
| `Medico_ID_Apertura` | `INT UNSIGNED` | No | FK a `tbb_hr_personal_medico.ID` | - | Medico que abre el expediente |
| `Seguro_Proveedor_ID` | `INT UNSIGNED` | Si | Referencia simulada sin FK | `NULL` | Proveedor de seguro |
| `fecha_apertura` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Apertura |
| `estatus_expediente` | `ENUM('Activo','Inactivo','Archivo Muerto','Retenido Legalmente')` | Si | - | `'Activo'` | Estado |
| `nivel_confidencialidad` | `ENUM('Normal','Restringido','Estricto')` | Si | - | `'Normal'` | Nivel de acceso |
| `antecedentes_historial_clinico` | `TEXT` | Si | - | `NULL` | Antecedentes fusionados |
| `evaluacion_inicial_ingreso` | `TEXT` | Si | - | `NULL` | Evaluacion de ingreso |
| `tiene_consentimiento_informado` | `BIT(1)` | No | - | `b'0'` | Consentimiento |
| `detalles_seguro_poliza` | `VARCHAR(200)` | Si | - | `NULL` | Resumen de poliza |
| `alertas_medicas_criticas` | `VARCHAR(255)` | Si | - | `NULL` | Alertas del expediente |

`Paciente_ID` usa eliminacion `RESTRICT`. `Medico_ID_Apertura` conserva el
comportamiento restrictivo por defecto de MySQL.

### 6.4 `tbb_md_notas_medicas`

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `ID` | `INT UNSIGNED` | No | PK, AI | - | Identificador |
| `FechaRegistro` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Fecha de generacion |
| `Estatus` | `BIT(1)` | No | - | `b'1'` | Estado logico |
| `TipoNota` | `VARCHAR(50)` | No | - | - | Tipo solicitado en la prueba |
| `AntecedentesRelevantes` | `TEXT` | Si | - | `NULL` | Antecedentes generados |
| `SintomasActuales` | `TEXT` | No | - | - | Sintomas generados |
| `InterrogatorioAnamnesis` | `TEXT` | No | - | - | Interrogatorio generado |
| `SignosVitales` | `ENUM(...)` | No | Catalogo de seis textos predefinidos | `'No recabados'` | Resumen de signos |
| `Auditoria` | `VARCHAR(255)` | No | - | `'Sistema'` | Resultado de auditoria clinica |
| `Paciente_ID` | `INT UNSIGNED` | No | FK a `tbb_md_pacientes.ID` | - | Paciente |
| `Medico_ID` | `INT UNSIGNED` | No | FK a `tbb_hr_personal_medico.ID` | - | Medico |
| `Expediente_ID` | `INT UNSIGNED` | No | FK a `tbb_md_expedientes_medicos.ID` | - | Expediente |

### 6.5 `tbi_bitacora`

Bitacora resumida de operaciones de las pruebas SQL.

| Campo | Tipo | Nulo | Llave o regla | Defecto | Descripcion |
| --- | --- | --- | --- | --- | --- |
| `ID` | `INT UNSIGNED` | No | PK, AI | - | Identificador |
| `usuario` | `VARCHAR(100)` | No | - | - | Usuario o IP solicitante |
| `NombreTabla` | `VARCHAR(100)` | No | - | - | Tabla afectada |
| `Operacion` | `VARCHAR(50)` | No | - | - | Tipo de operacion |
| `Descripcion` | `TEXT` | Si | - | `NULL` | Resumen |
| `fechaHora` | `DATETIME` | No | - | `CURRENT_TIMESTAMP` | Fecha del evento |

## 7. Rutinas SQL para Simulacion

Las rutinas ubicadas en `DataBases/SQL/Functions` y
`DataBases/SQL/StoredProcedures` generan informacion sintetica para poblar
`tbb_md_notas_medicas`.

| Rutina | Tipo | Parametros | Retorno o efecto |
| --- | --- | --- | --- |
| `fn_generar_antecedentes` | Funcion | `p_es_paciente_zero BOOLEAN` | Antecedentes clinicos sinteticos o `NULL` |
| `fn_generar_auditoria` | Funcion | `p_usuario_ip VARCHAR(100)` | Texto de auditoria clinica |
| `fn_generar_interrogatorio` | Funcion | `p_es_paciente_zero BOOLEAN`, `p_genero VARCHAR(15)`, `p_edad INT` | Interrogatorio sintetico |
| `fn_generar_signos_vitales` | Funcion | `p_es_paciente_zero BOOLEAN`, `p_escenario VARCHAR(30)` | Resumen de signos vitales |
| `fn_generar_sintomas` | Funcion | `p_es_paciente_zero BOOLEAN` | Sintomas sinteticos |
| `fn_generar_tipo_nota` | Funcion | Sin parametros | Tipo de nota aleatorio |
| `sp_poblar_notas_dinamico` | Procedimiento | Cantidad, tipos de nota, banderas de pediatria, UCI y paciente zero, usuario o IP | Inserta notas masivas y un resumen en `tbi_bitacora` |

## 8. Observaciones de Mantenimiento

- La fuente de verdad del esquema principal es
  `Deliverables/API/source/init_db.sql`, alineada con
  `Deliverables/API/source/models.py`.
- Las validaciones declaradas solo en Pydantic se identifican como reglas de
  aplicacion; no deben confundirse con restricciones DDL.
- `md_signos_vitales.score_mews` se calcula en la API, no mediante un trigger.
- `md_tratamientos.fecha_fin` es un dato opcional persistido; el DDL no incluye
  una columna calculada.
- `Seguro_Proveedor_ID` y `Area_ID` del esquema de volumen son referencias
  simuladas sin FK declarada.
- El diccionario NoSQL se mantiene por separado en
  `DataBases/NoSQL/DD/README.md`.

## 9. Catalogos y Reglas de Negocio

### 9.1 Roles de usuario

| Valor | Descripcion |
| --- | --- |
| `admin` | Administracion de usuarios y acceso completo al sistema |
| `medico` | Operacion clinica sobre notas, diagnosticos y tratamientos |
| `enfermero` | Registro de signos vitales y consulta de informacion clinica |

### 9.2 Tipos de nota medica

| Valor | Descripcion |
| --- | --- |
| `ingreso` | Evaluacion inicial al admitir al paciente |
| `evolucion` | Seguimiento de la condicion clinica |
| `egreso` | Resumen generado al dar de alta al paciente |
| `interconsulta` | Valoracion solicitada a otro especialista |
| `urgencias` | Atencion proporcionada por el servicio de urgencias |

### 9.3 Calculo MEWS

El puntaje `md_signos_vitales.score_mews` se calcula en la API antes de
insertar la toma. Los umbrales implementados en `utils/helpers.py` son:

| Parametro | Condicion | Puntos |
| --- | --- | --- |
| Frecuencia cardiaca | `< 40` o `> 130` lpm | `+2` |
| Frecuencia cardiaca | `< 50` o `> 110` lpm | `+1` |
| Frecuencia respiratoria | `< 9` o `> 30` rpm | `+3` |
| Frecuencia respiratoria | `> 20` rpm | `+1` |
| Saturacion de oxigeno | `< 85%` | `+3` |
| Saturacion de oxigeno | `< 90%` | `+2` |
| Saturacion de oxigeno | `< 95%` | `+1` |
| Temperatura | `< 35.0` o `> 39.0` grados Celsius | `+2` |
| Temperatura | `< 36.0` o `> 38.5` grados Celsius | `+1` |
| Consciencia | Contiene `inconsciente` o `coma` | `+3` |
| Consciencia | Contiene `confuso` o `somnoliento` | `+2` |
| Consciencia | Contiene `desorientado` | `+1` |

| Puntaje total | Clasificacion API |
| --- | --- |
| `0..4` | `NORMAL` |
| `5..6` | `MODERADO` |
| `>= 7` | `CRITICO` |

Un puntaje mayor o igual a `5` genera una alerta en la coleccion MongoDB
`valoraciones_flexibles`.

### 9.4 Codigos CIE-10

La API valida `md_diagnostico.codigo_cie` antes de insertar el diagnostico.
Ejemplos de valores compatibles con el patron configurado:

| Codigo | Ejemplo de diagnostico |
| --- | --- |
| `J18.9` | Neumonia no especificada |
| `I10` | Hipertension esencial |
| `E11.9` | Diabetes mellitus tipo 2 sin complicaciones |
| `K29.7` | Gastritis no especificada |
| `S06.0` | Conmocion cerebral |

### 9.5 Escalas clinicas

`md_valoraciones.escala` admite `Glasgow`, `MEWS`, `APGAR`, `Braden`,
`Norton` y `SOFA`. La API incluye una clasificacion auxiliar para Glasgow:

| Escala Glasgow | Clasificacion |
| --- | --- |
| `13..15` | Leve |
| `9..12` | Moderado |
| `< 9` | Grave |

Las interpretaciones detalladas del resto de las escalas deben mantenerse en
la capa clinica correspondiente. El DDL solo restringe el catalogo de nombres.

## 10. Archivos de Referencia

| Archivo | Contenido |
| --- | --- |
| `Deliverables/API/source/init_db.sql` | DDL del esquema principal |
| `Deliverables/API/source/models.py` | Modelos ORM SQLAlchemy |
| `Deliverables/API/source/schemas.py` | Validaciones de entrada y salida |
| `Deliverables/API/source/utils/helpers.py` | Calculo MEWS |
| `Deliverables/API/source/volume_tests/config/db_mysql.py` | DDL y semilla del esquema de volumen |
| `DataBases/SQL/Functions/*.sql` | Funciones para datos sinteticos |
| `DataBases/SQL/StoredProcedures/sp_poblar_notas_dinamico.sql` | Insercion masiva de notas |

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |