# Schemas

## Descripcion general

La carpeta `Schemas` concentra las definiciones estructurales y las reglas de validacion para los documentos de la base de datos NoSQL del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es centralizar la logica que rige la entrada y modificacion de datos, asegurando la consistencia dentro de un entorno de esquema flexible.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar los archivos de definicion (ej. esquemas y modelos de Mongoose, o JSON Schema);
- conservar las restricciones, validadores personalizados y expresiones regulares;
- facilitar la auditoria de los tipos de datos admitidos en cada coleccion;
- asegurar la sincronizacion entre las reglas del backend y la base de datos.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| *No aplica* | Los archivos de esquema se guardan directamente en este nivel. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- scripts con la declaracion de esquemas en el lenguaje del proyecto (ej. `.js` o `.ts`);
- funciones de validacion personalizadas y middleware asociado a los esquemas (pre/post hooks);
- metadatos de configuracion para indices, propiedades unicas y marcas de tiempo (timestamps).

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- usar nombres de archivo que identifiquen sin ambiguedades la coleccion (ej. `patientSchema.js`);
- documentar mediante comentarios las razones detras de restricciones de negocio complejas;
- mantener estricta coherencia entre los esquemas programaticos aqui definidos y los diccionarios en la carpeta `DD`;
- organizar las propiedades de forma logica, agrupando campos relacionados.

### TABLA DE COLABORADORES
| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |