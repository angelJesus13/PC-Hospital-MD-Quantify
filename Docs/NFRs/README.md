# Requerimientos No Funcionales (NFRs) ![Microsoft Word](https://camo.githubusercontent.com/beb29946b4a70724ef7b9bcbccb3420a4c96905bdbb1d2f3c40941ade6156d67/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d6963726f736f66745f576f72642d3242353739413f7374796c653d666f722d7468652d6261646765266c6f676f3d6d6963726f736f66742d776f7264266c6f676f436f6c6f723d7768697465)

Este directorio está destinado a almacenar y estructurar los **Requerimientos No Funcionales (Non-Functional Requirements - NFRs)** del ecosistema **Quantify**.

---

## Definición de Requerimientos No Funcionales

Los **Requerimientos No Funcionales (NFRs)** determinan los atributos de calidad, estándares técnicos y restricciones operativas bajo las cuales debe operar un sistema de software. No detallan funciones particulares, sino que responden a la pregunta: **¿Cómo debe comportarse y rendir el sistema en general?**

En el ecosistema **Quantify**, los requerimientos no funcionales especifican:
*   **Desempeño y Velocidad:** Tiempos máximos de respuesta de la API y rendimiento analítico al consultar millones de registros de logs.
*   **Escalabilidad Híbrida:** Tolerancia y separación de cargas entre la base de datos SQL transaccional y la base de datos NoSQL MongoDB.
*   **Seguridad y Privacidad:** Protocolos de cifrado de credenciales, seguridad en transporte (HTTPS/SSL) y autorización robusta.
*   **Estética y Diseño:** El cumplimiento de las pautas estilísticas del *Engineering Aesthetic* (tiempos de renderizado, animaciones fluidas).

---

## Contenido del Directorio

En esta carpeta se almacenarán próximamente los siguientes entregables y documentos oficiales:
*   📄 **Quantify_NonFunctional_Requirements.docx / .pdf**: Documento formal maestro que detalla las métricas de rendimiento, arquitectura de infraestructura y directrices de seguridad.
*   📄 **Performance_Benchmarks**: Informes y telemetría arrojados por las simulaciones analíticas con 300,000 registros.

---

## Estructura de Documentación

A continuación se presenta la arquitectura de carpetas del repositorio, destacando de forma interactiva tu ubicación actual:

*   📂 **PC-Hospital-MD-Quantify/**
    *   📁 `DataBases/`
    *   📁 `DataModels/`
    *   📁 `Deliverables/`
    *   📂 `Docs/`
        *   📁 `BRs/`
        *   📁 `FRs/`
        *   📁 `GUIs/`
        *   📂 **NFRs/**  ◄── 
            *   📄 `.gitkeep`
            *   📄 **README.md**  ◄── 
        *   📁 `UHs/`
        *   📁 `URs/`

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Completado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | En revisión |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En revisión |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En revisión |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | En revisión |