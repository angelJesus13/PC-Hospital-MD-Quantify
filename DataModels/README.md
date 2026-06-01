# DataModels

## Descripcion general

La carpeta `DataModels` centraliza la documentacion y los artefactos futuros de
los modelos analiticos de `PC-Hospital-MD-Quantify`. Su objetivo es mantener
trazabilidad entre las fuentes SQL y NoSQL, los problemas analiticos, las
variables utilizadas y la evidencia de evaluacion.

Actualmente el repositorio contiene reglas clinicas deterministas y una
propuesta documentada de modelos supervisados y no supervisados. Todavia no se
incluyen modelos entrenados, notebooks de entrenamiento ni artefactos
serializados.

## Documento principal

La especificacion completa se encuentra en:

- [`Data_Model_Documentation.md`](Data_Model_Documentation.md)

Este documento describe:

- la arquitectura de datos disponible;
- las reglas analiticas ya implementadas en la API;
- los modelos supervisados y no supervisados propuestos;
- las variables, fuentes y metricas recomendadas;
- el flujo de preparacion de datos;
- las consideraciones de seguridad para informacion clinica.

## Estructura existente

| Ruta | Uso |
| --- | --- |
| `Data_Model_Documentation.md` | Catalogo general y trazabilidad de modelos |
| `Supervised_LMs/` | Espacio para modelos supervisados futuros |
| `Unsupervised_LMs/` | Espacio para modelos no supervisados futuros |

## Modelos documentados

| ID | Modelo | Tipo | Estado |
| --- | --- | --- | --- |
| `SUP-01` | Riesgo de deterioro clinico | Supervisado | Propuesto |
| `SUP-02` | Priorizacion de severidad diagnostica | Supervisado | Propuesto |
| `UNS-01` | Segmentacion de perfiles clinicos | No supervisado | Propuesto |
| `UNS-02` | Deteccion de patrones atipicos | No supervisado | Propuesto |

## Lineamientos

- Documentar la fuente y el rango temporal de los datos.
- Mantener separados los datos sinteticos y los datos clinicos reales.
- Evitar datos personales identificables en los datasets de entrenamiento.
- Registrar variables, metricas, limitaciones y version de cada modelo.
- Conservar evidencia reproducible en la carpeta correspondiente.

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | Revisado y Aprobado |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | Aprobado confirmado |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
