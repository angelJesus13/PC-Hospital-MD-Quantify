# ERD - MERE y MER

## Descripcion general

Esta carpeta contiene la documentacion y evidencias del modelado entidad-relacion del proyecto **PC-Hospital-MD-Quantify**. Aqui deben colocarse los diagramas correspondientes al **MERE** y al **MER** utilizados para representar la estructura conceptual de la base de datos SQL.

## Objetivo

El objetivo de esta carpeta es conservar los diagramas que explican las entidades, atributos, relaciones y cardinalidades principales del sistema antes de transformarlas al modelo relacional.

## Contenido esperado

| Archivo o recurso | Descripcion |
| --- | --- |
| `MERE_Quantify.png` o `.pdf` | Modelo Entidad-Relacion Extendido con especializaciones y reglas generales. |
| `MER_Quantify.png` o `.pdf` | Modelo Entidad-Relacion final con entidades, atributos y relaciones. |
| `README.md` | Documento base de referencia para esta carpeta. |

## Entidades principales

| Entidad | Descripcion |
| --- | --- |
| Usuario | Representa a una persona con acceso al sistema. |
| Rol | Define permisos y tipo de usuario. |
| Paciente | Representa al usuario monitoreado clinica u operativamente. |
| ProfesionalSalud | Representa al personal que consulta o supervisa informacion del paciente. |
| DispositivoWearable | Representa un dispositivo vinculado al paciente. |
| MedicionBiometrica | Representa mediciones capturadas por el wearable. |
| LogActividad | Representa registros diarios de actividad o disciplina. |
| Alerta | Representa notificaciones generadas por condiciones relevantes. |
| Sesion | Representa accesos o sesiones de usuario. |

## Relaciones principales

| Relacion | Cardinalidad | Descripcion |
| --- | --- | --- |
| Usuario - Rol | N:1 | Muchos usuarios pueden compartir un rol. |
| Usuario - Paciente | 1:0..1 | Un usuario puede tener perfil de paciente. |
| Usuario - ProfesionalSalud | 1:0..1 | Un usuario puede tener perfil profesional. |
| Paciente - DispositivoWearable | 1:N | Un paciente puede registrar varios dispositivos. |
| DispositivoWearable - MedicionBiometrica | 1:N | Un dispositivo puede generar multiples mediciones. |
| Paciente - LogActividad | 1:N | Un paciente puede tener multiples registros historicos. |
| Paciente - Alerta | 1:N | Un paciente puede recibir multiples alertas. |
| ProfesionalSalud - Paciente | N:M | Un profesional puede revisar varios pacientes y viceversa. |

## Estado

Carpeta preparada para recibir los diagramas MERE y MER del proyecto.
