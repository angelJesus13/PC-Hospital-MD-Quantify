# ERD

## Descripcion general

La carpeta `ERD` (Entity-Relationship Diagrams) contiene la representacion visual y conceptual de la arquitectura de la base de datos relacional del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es proporcionar un mapa de alto nivel de las entidades del sistema y las interacciones entre ellas antes de llegar a la implementacion fisica.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar los diagramas conceptuales que modelan las reglas de negocio;
- conservar la visibilidad grafica de la cardinalidad de las relaciones (1:1, 1:N, N:M);
- facilitar las reuniones de diseño arquitectonico con stakeholders;
- apoyar la planeacion de nuevas funcionalidades que impacten la base de datos.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| *No aplica* | Las imagenes y archivos fuente se almacenan en este nivel. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- imagenes exportadas de los diagramas (en formato `.png`, `.jpg` o `.pdf`);
- archivos fuente editables generados por herramientas de modelado (ej. `.drawio`, `.vsdx`, `.mwb`);
- notas aclaratorias sobre decisiones de diseño complejas que no sean evidentes en el diagrama.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- exportar siempre una version en imagen (.png o .pdf) junto con el archivo fuente, para facilitar su visualizacion en la web;
- usar notacion estandar (como Pata de Cuervo / Crow's Foot) para definir claramente la cardinalidad;
- actualizar los diagramas de inmediato si se aprueba un cambio estructural en el modelo de datos;
- nombrar los archivos incluyendo el modulo o area que cubren, si el diagrama completo es demasiado grande (ej. `ERD_ModuloFacturacion.png`).

### TABLA DE COLABORADORES
| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |