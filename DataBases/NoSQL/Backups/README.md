# Backups

## Descripcion general

La carpeta `Backups` centraliza las copias de seguridad de las colecciones de la base de datos NoSQL del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es garantizar la disponibilidad y recuperacion de los datos en caso de contingencias, perdida de informacion o necesidad de restaurar el estado del sistema a un punto anterior.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar volcados de datos (dumps) y exportaciones de colecciones;
- conservar historicos de la informacion no relacional del sistema;
- facilitar los procesos de restauracion y migracion entre entornos (desarrollo, pruebas, produccion);
- apoyar las auditorias de integridad de datos.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| *No aplica* | Los archivos se almacenan en la raiz de este directorio o categorizados por formato/fecha sin subcarpetas fijas. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- archivos de exportacion en formatos nativos (BSON, JSON) o comprimidos;
- scripts automatizados para la generacion y carga de respaldos;
- bitacoras (logs) de ejecucion de copias de seguridad;
- manuales breves de comandos de restauracion (ej. mongorestore).

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- usar convenciones de nomenclatura que incluyan fecha y hora (ej. `backup_YYYYMMDD_HHMM.archive`);
- documentar el entorno de origen del respaldo (produccion, staging, local);
- mantener un limite razonable de retencion de archivos para optimizar el espacio en el repositorio;
- validar periodicamente que los archivos almacenados se puedan restaurar exitosamente.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
