# Backups

## Descripcion general

La carpeta `Backups` centraliza las copias de seguridad, volcados de datos (dumps) y exportaciones estructurales de la base de datos relacional del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es resguardar la informacion transaccional y la arquitectura de las tablas para garantizar la recuperacion ante desastres o facilitar la clonacion de entornos de desarrollo.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar los archivos `.sql`, `.bak` o comprimidos con la informacion y estructura del sistema;
- conservar puntos de restauracion (snapshots) previos a migraciones o actualizaciones mayores;
- facilitar la recuperacion de la informacion operativa y transaccional;
- apoyar los procesos de auditoria de bases de datos.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| *No aplica* | Los archivos de respaldo se almacenan directamente en esta raiz, preferentemente organizados por fecha en su nombre. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- archivos de volcado completo de la base de datos (estructura y datos);
- scripts para respaldos unicamente estructurales (sin datos sensibles);
- bitacoras de procesos automatizados de respaldo;
- manuales o comandos rapidos de restauracion para los motores SQL utilizados.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- usar convenciones de nomenclatura estrictas que incluyan fecha y hora (ej. `db_backup_YYYYMMDD_HHMM.sql`);
- documentar si el respaldo pertenece al entorno de produccion, pruebas o desarrollo;
- considerar politicas de privacidad y estandares internacionales en la manipulacion de estos archivos, recordando la naturaleza de empresa extranjera del proyecto;
- purgar periodicamente respaldos muy antiguos para no saturar el repositorio, si no se usa un almacenamiento externo.

### TABLA DE COLABORADORES
| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |