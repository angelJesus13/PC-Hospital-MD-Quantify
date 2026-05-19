# DataBases

## Descripcion general

La carpeta `DataBases` centraliza todos los artefactos de diseño, arquitectura y persistencia de datos del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es mantener organizados los modelos, esquemas, diccionarios y respaldos que garantizan la integridad, disponibilidad y estructura de la informacion del sistema, abarcando tanto enfoques relacionales como no relacionales.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar los modelos conceptuales, logicos y fisicos de las bases de datos;
- conservar las definiciones exactas de las estructuras de datos y diccionarios;
- facilitar el mantenimiento, migracion y escalabilidad de la persistencia de datos;
- organizar las politicas y archivos de respaldo (backups) del entorno de base de datos.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| `NoSQL/` | Artefactos, esquemas y respaldos relacionados con las bases de datos no relacionales orientadas a documentos. |
| `SQL/` | Artefactos, diagramas y respaldos correspondientes a las bases de datos relacionales y transaccionales del proyecto. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- diagramas arquitectonicos de bases de datos;
- documentacion general de la infraestructura de datos;
- archivos de configuracion globales para conexiones o migraciones.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- separar estrictamente los entornos relacionales de los no relacionales;
- asegurar que los esquemas y diccionarios reflejen la version mas actual en produccion;
- documentar cualquier cambio estructural que afecte el desarrollo de la API o las aplicaciones.