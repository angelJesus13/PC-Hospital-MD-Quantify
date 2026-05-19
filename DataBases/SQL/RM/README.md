# RM - Modelo Relacional

## Descripcion general

Esta carpeta contiene el **Modelo Relacional (RM)** derivado del MERE y MER del proyecto **PC-Hospital-MD-Quantify**. Su funcion es documentar como se transforman las entidades y relaciones en tablas, llaves primarias, llaves foraneas y restricciones.

## Modelo relacional propuesto

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

## Tablas principales

| Tabla | Proposito |
| --- | --- |
| `roles` | Catalogar permisos y perfiles del sistema. |
| `usuarios` | Registrar credenciales y datos generales de acceso. |
| `pacientes` | Guardar informacion especifica de pacientes. |
| `profesionales_salud` | Guardar informacion de personal medico o supervisor. |
| `paciente_profesional` | Resolver la relacion muchos a muchos entre pacientes y profesionales. |
| `dispositivos_wearable` | Registrar dispositivos asociados a pacientes. |
| `mediciones_biometricas` | Guardar mediciones capturadas por dispositivos. |
| `logs_actividad` | Registrar actividad diaria o eventos de disciplina. |
| `alertas` | Guardar alertas generadas por reglas del sistema. |
| `sesiones` | Registrar accesos y sesiones de usuarios. |

## Reglas de normalizacion

- Cada tabla debe tener una llave primaria.
- Las relaciones N:M deben resolverse mediante tablas intermedias.
- Los datos de usuario, paciente y profesional deben mantenerse separados para evitar redundancia.
- Las mediciones biometricas deben conservar referencia al paciente y al dispositivo.
- Los catalogos como roles o estados deben evitar valores inconsistentes.

## Estado

Documento base preparado para representar el modelo relacional del proyecto.
