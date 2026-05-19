# DD

## Descripcion general

La carpeta `DD` (Diccionarios de Datos) almacena la documentacion exhaustiva de cada tabla, columna y relacion que conforma la base de datos SQL del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es servir como el glosario definitivo que estandariza la comprension del esquema relacional, las restricciones y las reglas de negocio implementadas a nivel de base de datos.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar las definiciones exactas de tipos de datos, longitudes y restricciones (NOT NULL, UNIQUE);
- conservar la justificacion y mapeo de las llaves primarias (PK) y foraneas (FK);
- facilitar el entendimiento del modelo a nuevos desarrolladores o analistas;
- apoyar la validacion de requisitos y la generacion de consultas complejas.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| *No aplica* | Los diccionarios se guardan como archivos individuales en esta ubicacion. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- documentos en formato Markdown, Excel o CSV con matrices de datos;
- glosarios de terminos y abreviaturas utilizadas en el nombramiento de las tablas;
- descripciones de valores admitidos para campos de tipo ENUM o catalogos.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- mantener el diccionario estrictamente sincronizado con la version en produccion de la base de datos;
- definir de manera inequivoca la entidad que representa cada tabla (por ejemplo, especificando claramente cuando una tabla representa entidades operativas o administrativas y no asumir por defecto que se trata de pacientes u otros perfiles);
- detallar el proposito de las restricciones y llaves, especialmente en relaciones de muchos a muchos;
- utilizar un formato tabular para facilitar la lectura rapida de campos y tipos.

### TABLA DE COLABORADORES
| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |