# DataModels

## Descripcion general

La carpeta `DataModels` centraliza los artefactos relacionados con el modelado de datos y el analisis inteligente del proyecto `PC-Hospital-MD-Quantify`. Su objetivo es mantener organizados los recursos utilizados para entrenar, evaluar y documentar los modelos que apoyan la interpretacion de la informacion clinica y operativa del sistema.

## Objetivo

Esta seccion del repositorio sirve como punto de referencia para:

- almacenar modelos desarrollados durante el proyecto;
- conservar evidencia de experimentacion y evaluacion;
- facilitar la trazabilidad de resultados;
- apoyar la reproducibilidad del trabajo analitico.

## Estructura de carpetas

| Carpeta | Descripcion |
| --- | --- |
| `Supervised_LMs/` | Modelos supervisados, entrenados con una variable objetivo conocida. |
| `Unsupervised_LMs/` | Modelos no supervisados enfocados en descubrimiento de patrones, agrupamientos o estructura oculta en los datos. |

## Contenido esperado

Dentro de esta carpeta pueden incluirse:

- notebooks de exploracion, entrenamiento o validacion;
- scripts de preprocesamiento y modelado;
- modelos exportados o serializados;
- reportes de resultados;
- graficas, metricas y evidencia experimental.

## Documentacion de modelos de datos

El documento principal de modelado se encuentra en:

- [`Data_Model_Documentation.md`](Data_Model_Documentation.md)

Este archivo concentra la descripcion del MERE, MER, modelo relacional, diccionarios de datos SQL/NoSQL y schemas propuestos para el proyecto.

## Lineamientos de documentacion

Para mantener esta seccion clara y util, se recomienda:

- usar nombres descriptivos para archivos y carpetas;
- documentar el origen de los datos utilizados;
- registrar metricas relevantes por experimento;
- mantener evidencia suficiente para reproducir entrenamientos y pruebas.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Aprobado |

