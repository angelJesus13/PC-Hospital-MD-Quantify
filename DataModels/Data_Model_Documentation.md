# Documentacion de Modelos de Datos

## Descripcion general

Este documento concentra la documentacion base de los modelos de datos del proyecto **PC-Hospital-MD-Quantify**. Incluye la descripcion del MERE, MER, diccionario de datos y schemas necesarios para entender la estructura de informacion del sistema.

El objetivo es dejar una referencia clara para el analisis de datos, la implementacion de bases de datos SQL/NoSQL y la integracion con la API.

## Alcance

La documentacion cubre:

- Modelo Entidad-Relacion Extendido (MERE);
- Modelo Entidad-Relacion (MER);
- modelo relacional;
- diccionario de datos SQL;
- diccionario de datos NoSQL;
- schemas de colecciones NoSQL;
- relacion entre datos operativos y datos analiticos.

## Arquitectura de datos propuesta

El proyecto contempla una arquitectura hibrida:

| Componente | Tecnologia sugerida | Proposito |
| --- | --- | --- |
| Base de datos SQL | MySQL o equivalente relacional | Gestion transaccional de usuarios, pacientes, roles, sesiones y catalogos. |
| Base de datos NoSQL | MongoDB o equivalente documental | Almacenamiento flexible de logs, biometria, eventos de wearable y registros historicos. |
| API | Backend del proyecto | Punto de acceso para consultar, registrar y sincronizar informacion. |
| DataModels | Modelos analiticos | Analisis, prediccion, segmentacion o interpretacion de informacion del sistema. |

## MERE - Modelo Entidad-Relacion Extendido

El MERE representa las entidades principales del sistema, sus atributos clave, relaciones y posibles especializaciones. Para el contexto de Hospital MD / Quantify, se proponen las siguientes entidades base.

| Entidad | Descripcion | Tipo |
| --- | --- | --- |
| Usuario | Persona registrada en el sistema con credenciales y permisos de acceso. | Entidad fuerte |
| Rol | Clasificacion de permisos asignados a usuarios. | Catalogo |
| Paciente | Persona monitoreada por el sistema. | Entidad fuerte |
| ProfesionalSalud | Usuario especializado que revisa informacion clinica o de seguimiento. | Especializacion de Usuario |
| DispositivoWearable | Dispositivo asociado a un paciente para capturar informacion. | Entidad fuerte |
| MedicionBiometrica | Registro de datos capturados por el wearable. | Entidad debil o transaccional |
| LogActividad | Registro de actividad, comportamiento o disciplina diaria. | Entidad transaccional |
| Alerta | Notificacion generada por valores fuera de rango o eventos relevantes. | Entidad transaccional |
| Sesion | Registro de autenticacion y actividad de usuario. | Entidad transaccional |

### Especializaciones sugeridas

| Entidad general | Especializacion | Descripcion |
| --- | --- | --- |
| Usuario | Administrador | Gestiona configuracion, usuarios y supervision general. |
| Usuario | ProfesionalSalud | Consulta informacion de pacientes y seguimiento. |
| Usuario | Paciente | Consulta sus datos, alertas o progreso personal. |

### Relaciones principales

| Relacion | Cardinalidad | Descripcion |
| --- | --- | --- |
| Usuario - Rol | N:1 | Un usuario tiene un rol principal; un rol puede pertenecer a muchos usuarios. |
| Paciente - DispositivoWearable | 1:N | Un paciente puede tener uno o varios dispositivos asociados. |
| DispositivoWearable - MedicionBiometrica | 1:N | Un dispositivo genera multiples mediciones. |
| Paciente - LogActividad | 1:N | Un paciente puede tener multiples registros de actividad. |
| Paciente - Alerta | 1:N | Un paciente puede recibir multiples alertas. |
| ProfesionalSalud - Paciente | N:M | Un profesional puede revisar varios pacientes y un paciente puede ser revisado por varios profesionales. |
| Usuario - Sesion | 1:N | Un usuario puede iniciar multiples sesiones. |

## MER - Modelo Entidad-Relacion

El MER transforma la vision extendida en una estructura relacional mas directa. Las entidades propuestas pueden representarse como tablas normalizadas.

| Tabla | Llave primaria | Llaves foraneas | Descripcion |
| --- | --- | --- | --- |
| `roles` | `id_rol` | Ninguna | Catalogo de roles del sistema. |
| `usuarios` | `id_usuario` | `id_rol` | Credenciales y datos generales de usuarios. |
| `pacientes` | `id_paciente` | `id_usuario` | Informacion especifica del paciente. |
| `profesionales_salud` | `id_profesional` | `id_usuario` | Informacion del personal de salud. |
| `paciente_profesional` | `id_paciente_profesional` | `id_paciente`, `id_profesional` | Relacion entre pacientes y profesionales. |
| `dispositivos_wearable` | `id_dispositivo` | `id_paciente` | Dispositivos vinculados a pacientes. |
| `mediciones_biometricas` | `id_medicion` | `id_dispositivo`, `id_paciente` | Mediciones de salud capturadas. |
| `logs_actividad` | `id_log` | `id_paciente` | Registros de actividad o disciplina. |
| `alertas` | `id_alerta` | `id_paciente`, `id_medicion` | Alertas generadas por reglas del sistema. |
| `sesiones` | `id_sesion` | `id_usuario` | Registro de sesiones y autenticacion. |

## Modelo relacional

```text
roles(id_rol PK, nombre, descripcion, activo)

usuarios(id_usuario PK, id_rol FK, nombre, correo, password_hash, estado, fecha_creacion)

pacientes(id_paciente PK, id_usuario FK, fecha_nacimiento, sexo, telefono, contacto_emergencia)

profesionales_salud(id_profesional PK, id_usuario FK, cedula, especialidad, telefono)

paciente_profesional(id_paciente_profesional PK, id_paciente FK, id_profesional FK, fecha_asignacion, estado)

dispositivos_wearable(id_dispositivo PK, id_paciente FK, tipo, marca, modelo, identificador, estado, fecha_vinculacion)

mediciones_biometricas(id_medicion PK, id_dispositivo FK, id_paciente FK, tipo_medicion, valor, unidad, fecha_registro)

logs_actividad(id_log PK, id_paciente FK, tipo_actividad, descripcion, valor, fecha_registro)

alertas(id_alerta PK, id_paciente FK, id_medicion FK, tipo_alerta, mensaje, severidad, estado, fecha_creacion)

sesiones(id_sesion PK, id_usuario FK, token_hash, fecha_inicio, fecha_fin, ip_origen, estado)
```

## Diccionario de datos SQL

### Tabla `usuarios`

| Campo | Tipo sugerido | Restricciones | Descripcion |
| --- | --- | --- | --- |
| `id_usuario` | INT | PK, AI | Identificador unico del usuario. |
| `id_rol` | INT | FK, NOT NULL | Rol asignado al usuario. |
| `nombre` | VARCHAR(120) | NOT NULL | Nombre completo del usuario. |
| `correo` | VARCHAR(120) | UNIQUE, NOT NULL | Correo usado para autenticacion. |
| `password_hash` | VARCHAR(255) | NOT NULL | Contrasena cifrada o hasheada. |
| `estado` | VARCHAR(20) | NOT NULL | Estado del usuario: activo, inactivo o bloqueado. |
| `fecha_creacion` | DATETIME | NOT NULL | Fecha de registro. |

### Tabla `pacientes`

| Campo | Tipo sugerido | Restricciones | Descripcion |
| --- | --- | --- | --- |
| `id_paciente` | INT | PK, AI | Identificador unico del paciente. |
| `id_usuario` | INT | FK, NOT NULL | Usuario asociado al paciente. |
| `fecha_nacimiento` | DATE | NULL | Fecha de nacimiento. |
| `sexo` | VARCHAR(20) | NULL | Sexo registrado. |
| `telefono` | VARCHAR(20) | NULL | Telefono de contacto. |
| `contacto_emergencia` | VARCHAR(120) | NULL | Contacto para emergencia. |

### Tabla `dispositivos_wearable`

| Campo | Tipo sugerido | Restricciones | Descripcion |
| --- | --- | --- | --- |
| `id_dispositivo` | INT | PK, AI | Identificador del dispositivo. |
| `id_paciente` | INT | FK, NOT NULL | Paciente propietario o vinculado. |
| `tipo` | VARCHAR(50) | NOT NULL | Tipo de dispositivo wearable. |
| `marca` | VARCHAR(80) | NULL | Marca del dispositivo. |
| `modelo` | VARCHAR(80) | NULL | Modelo del dispositivo. |
| `identificador` | VARCHAR(120) | UNIQUE | Identificador fisico o logico del wearable. |
| `estado` | VARCHAR(20) | NOT NULL | Estado: activo, inactivo, mantenimiento. |
| `fecha_vinculacion` | DATETIME | NOT NULL | Fecha en que se vinculo al paciente. |

### Tabla `mediciones_biometricas`

| Campo | Tipo sugerido | Restricciones | Descripcion |
| --- | --- | --- | --- |
| `id_medicion` | BIGINT | PK, AI | Identificador de la medicion. |
| `id_dispositivo` | INT | FK, NOT NULL | Dispositivo que genero el dato. |
| `id_paciente` | INT | FK, NOT NULL | Paciente relacionado. |
| `tipo_medicion` | VARCHAR(60) | NOT NULL | Tipo: ritmo_cardiaco, pasos, oxigenacion, sueno, etc. |
| `valor` | DECIMAL(10,2) | NOT NULL | Valor numerico registrado. |
| `unidad` | VARCHAR(20) | NOT NULL | Unidad de medida. |
| `fecha_registro` | DATETIME | NOT NULL | Fecha y hora de captura. |

### Tabla `alertas`

| Campo | Tipo sugerido | Restricciones | Descripcion |
| --- | --- | --- | --- |
| `id_alerta` | BIGINT | PK, AI | Identificador de alerta. |
| `id_paciente` | INT | FK, NOT NULL | Paciente relacionado. |
| `id_medicion` | BIGINT | FK, NULL | Medicion que origino la alerta. |
| `tipo_alerta` | VARCHAR(60) | NOT NULL | Categoria de alerta. |
| `mensaje` | VARCHAR(255) | NOT NULL | Mensaje descriptivo. |
| `severidad` | VARCHAR(20) | NOT NULL | Nivel: baja, media, alta, critica. |
| `estado` | VARCHAR(20) | NOT NULL | Estado: nueva, revisada, cerrada. |
| `fecha_creacion` | DATETIME | NOT NULL | Fecha de generacion. |

## Schemas NoSQL

Los schemas NoSQL se proponen para informacion de alta frecuencia, historica o flexible. MongoDB permite almacenar documentos de mediciones, eventos y logs sin depender de una estructura tan rigida como SQL.

### Coleccion `wearable_logs`

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

### Coleccion `activity_logs`

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

### Coleccion `api_audit_logs`

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

## Diccionario de datos NoSQL

| Campo | Coleccion | Tipo | Descripcion |
| --- | --- | --- | --- |
| `patientId` | `wearable_logs`, `activity_logs` | number | Identificador del paciente relacionado. |
| `deviceId` | `wearable_logs` | number | Identificador del dispositivo wearable. |
| `eventType` | `wearable_logs` | string | Tipo de evento registrado por el wearable. |
| `payload` | `wearable_logs` | object | Contenedor flexible de mediciones capturadas. |
| `capturedAt` | `wearable_logs` | date | Fecha y hora en que se capturo la medicion. |
| `activityType` | `activity_logs` | string | Tipo de actividad registrada. |
| `streakCandidate` | `activity_logs` | boolean | Indica si el registro puede contar para una racha. |
| `endpoint` | `api_audit_logs` | string | Ruta de API consumida. |
| `statusCode` | `api_audit_logs` | number | Codigo HTTP de respuesta. |
| `responseTimeMs` | `api_audit_logs` | number | Tiempo de respuesta de la API. |

## Reglas de integridad

- Todo paciente debe estar asociado a un usuario valido.
- Toda medicion biometrica debe pertenecer a un paciente y, cuando aplique, a un dispositivo wearable.
- Las credenciales no deben almacenarse en texto plano.
- Las alertas deben relacionarse con un paciente y pueden relacionarse con una medicion especifica.
- Los logs NoSQL deben conservar fecha de captura para permitir analisis temporal.
- Los identificadores compartidos entre SQL y NoSQL deben conservar consistencia logica.

## Relacion con analisis de datos

Los modelos de datos documentados apoyan el analisis posterior mediante:

- historiales biometricos por paciente;
- deteccion de patrones de actividad;
- validacion de rachas o comportamiento;
- analisis de alertas recurrentes;
- medicion de rendimiento de API mediante logs;
- preparacion de datasets para modelos supervisados y no supervisados.

## Evidencia esperada en el repositorio

| Carpeta | Evidencia sugerida |
| --- | --- |
| `DataBases/SQL/ERD` | Diagramas MERE y MER en imagen, PDF o archivo editable. |
| `DataBases/SQL/RM` | Modelo relacional y normalizacion. |
| `DataBases/SQL/DD` | Diccionario de datos SQL. |
| `DataBases/NoSQL/Schemas` | Schemas JSON de colecciones NoSQL. |
| `DataBases/NoSQL/DD` | Diccionario de datos NoSQL. |
| `DataModels` | Documentacion analitica y trazabilidad hacia modelos de aprendizaje. |

## Estado

Documento base preparado para la practica del 19 de mayo de 2026. Puede actualizarse cuando se integren diagramas formales, scripts SQL, colecciones NoSQL o evidencias visuales.

## Equipo de desarrollo

| Integrante | Rol | Observaciones |
| --- | --- | --- |
| Angel de Jesus Baños Tellez | Lider de desarrollo | Revisado y aprobado |
| Francisco Garcia Garcia | Desarrollador | Revisado y aprobado |
| Jesus Alejandro Artiaga Morales | Desarrollador | Revisado y aprobado |
| Al Farias Leyva | Desarrollador | Revisado y aprobado |
| Brian Jesus Mendoza Marquez | Desarrollador | Revisado y aprobado |
