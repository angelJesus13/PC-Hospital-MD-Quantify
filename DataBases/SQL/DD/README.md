# DD - Diccionario de Datos SQL

## Descripcion general

Esta carpeta contiene el diccionario de datos para la base SQL del proyecto **PC-Hospital-MD-Quantify**. El diccionario describe tablas, campos, tipos de datos, restricciones y significado de cada elemento.

## Tablas documentadas

| Tabla | Descripcion |
| --- | --- |
| `roles` | Catalogo de perfiles y permisos. |
| `usuarios` | Datos generales y credenciales de acceso. |
| `pacientes` | Datos clinicos o personales basicos del paciente. |
| `profesionales_salud` | Informacion del personal encargado de revisar pacientes. |
| `paciente_profesional` | Relacion entre pacientes y profesionales. |
| `dispositivos_wearable` | Dispositivos asociados al monitoreo. |
| `mediciones_biometricas` | Mediciones generadas por dispositivos. |
| `logs_actividad` | Registros de actividad o disciplina. |
| `alertas` | Alertas generadas por eventos relevantes. |
| `sesiones` | Sesiones iniciadas por usuarios. |

## Campos criticos

| Campo | Tabla | Tipo sugerido | Reglas |
| --- | --- | --- | --- |
| `id_usuario` | `usuarios` | INT | PK, autoincremental. |
| `correo` | `usuarios` | VARCHAR(120) | Unico, obligatorio. |
| `password_hash` | `usuarios` | VARCHAR(255) | Obligatorio, no debe guardar texto plano. |
| `id_paciente` | `pacientes` | INT | PK, relacionado con usuario. |
| `id_dispositivo` | `dispositivos_wearable` | INT | PK, relacionado con paciente. |
| `tipo_medicion` | `mediciones_biometricas` | VARCHAR(60) | Obligatorio. |
| `valor` | `mediciones_biometricas` | DECIMAL(10,2) | Obligatorio. |
| `fecha_registro` | `mediciones_biometricas` | DATETIME | Obligatorio. |
| `severidad` | `alertas` | VARCHAR(20) | baja, media, alta o critica. |
| `estado` | `alertas` | VARCHAR(20) | nueva, revisada o cerrada. |

## Recomendaciones

- Mantener nombres de campos en minusculas y con guion bajo.
- Documentar cualquier cambio de tipo de dato.
- Agregar restricciones `NOT NULL` donde el negocio lo requiera.
- Usar indices en campos de busqueda frecuente como correo, paciente y fecha.

## Estado

Diccionario base preparado para ampliarse con scripts SQL o tablas finales.
