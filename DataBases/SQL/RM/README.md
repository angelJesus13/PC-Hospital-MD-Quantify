# RM

## Descripcion general

La carpeta `RM` (Modelos Relacionales) almacena la representacion fisica e implementacion final de la base de datos SQL del proyecto `PC-Hospital-MD-Quantify`. A diferencia del modelo conceptual (ERD), los modelos relacionales traducen las entidades y relaciones directamente a tablas, columnas, tipos de datos nativos del motor SQL y restricciones fisicas.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar la estructura tecnica y fisica de las tablas del sistema;
- conservar el mapeo exacto de las llaves primarias (PK) y llaves foraneas (FK);
- facilitar el puente entre el diseño conceptual y los scripts de creacion de bases de datos;
- apoyar a los administradores de bases de datos en la elaboracion de consultas, rutinas y optimizacion.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| *No aplica* | Los modelos y esquemas se guardan como archivos individuales en esta ubicacion. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- imagenes y esquemas relacionales generados a partir de herramientas de administracion de bases de datos (ej. Navicat, MySQL Workbench);
- representaciones graficas detalladas que incluyan tipos de datos, longitudes e indices fisicos;
- archivos de proyecto o fuentes del software de modelado orientados a la arquitectura de tablas.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- asegurar una correspondencia exacta entre este modelo relacional fisico, el diagrama conceptual (ERD) y el diccionario de datos (DD);
- exportar graficos de alta resolucion donde se puedan leer claramente todos los nombres de columnas y sus tipos de datos nativos (ej. VARCHAR, INT);
- actualizar inmediatamente estos esquemas si se modifican las tablas mediante migraciones o ajustes en la estructura;
- organizar o nombrar los archivos de manera que reflejen el subsistema o esquema especifico que documentan, si el modelo completo es muy extenso.

### TABLA DE COLABORADORES
| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |