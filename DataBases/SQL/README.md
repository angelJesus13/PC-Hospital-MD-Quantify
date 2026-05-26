# SQL

## Descripcion general

La subcarpeta `SQL` agrupa los recursos de diseño, modelado y resguardo de la base de datos relacional y transaccional del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es organizar todos los diagramas, scripts y diccionarios que aseguran la integridad referencial y las reglas de negocio a nivel base de datos.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar los diagramas de arquitectura relacional;
- conservar el modelo fisico y logico de las tablas del sistema;
- facilitar el acceso a scripts de creacion, modificacion y rutinas (SQL);
- centralizar las copias de seguridad de la base de datos transaccional.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| `Backups/` | Copias de seguridad (dumps) en formato SQL, historicos y puntos de restauracion. |
| `DD/` | Diccionarios de Datos definiendo tablas, columnas, tipos, restricciones y llaves foraneas. |
| `ERD/` | Diagramas Entidad-Relacion (Entity-Relationship Diagrams) para la conceptualizacion de entidades. |
| `RM/` | Modelos Relacionales (Relational Models), que muestran la implementacion fisica de las tablas. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- archivos de diagramas (`.png`, `.pdf` o nativos de herramientas de modelado);
- scripts `.sql` de creacion (DDL), migracion o consultas almacenadas (procedimientos, vistas);
- documentos tabulares (diccionarios) y manuales de restauracion.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- utilizar la nomenclatura estandar (mayusculas/minusculas) definida por el equipo para tablas y campos;
- actualizar invariablemente los diagramas (ERD y RM) cuando se agregue o modifique una tabla;
- registrar la fecha y la version en los archivos `.sql` de respaldos y migraciones;
- documentar claramente las restricciones y llaves primarias/foraneas en los diccionarios.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
