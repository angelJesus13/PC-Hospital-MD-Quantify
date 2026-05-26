# NoSQL

## Descripcion general

La subcarpeta `NoSQL` concentra los elementos de diseño, documentacion y respaldos especificos de la base de datos no relacional del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es estructurar la informacion que por su naturaleza requiere esquemas flexibles, alta disponibilidad y almacenamiento basado en documentos.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar la estructura JSON/BSON de las colecciones utilizadas;
- conservar los diccionarios de datos que describen los documentos;
- facilitar el versionado de validadores de esquemas;
- resguardar los respaldos especificos de este entorno no relacional.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| `Backups/` | Copias de seguridad, volcados (dumps) de colecciones y registros historicos de la base de datos NoSQL. |
| `DD/` | Diccionarios de Datos especificos de NoSQL, describiendo los campos, tipos y propositos de cada documento. |
| `Schemas/` | Archivos de definicion y reglas de validacion estructural para las colecciones (ej. esquemas de Mongoose/MongoDB). |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- scripts de creacion de colecciones e indices;
- archivos `.json` con datos semilla o estructura base;
- documentacion de politicas de fragmentacion (sharding) o replicacion si aplica.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- usar nombres descriptivos referenciando a la coleccion documentada;
- registrar detalladamente los tipos de datos en los diccionarios, considerando documentos anidados;
- mantener registros limpios y fechados de los respaldos;
- documentar el proposito de los indices creados en las colecciones.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |  Revisado y Aprobado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En Revision |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En Revision |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |

