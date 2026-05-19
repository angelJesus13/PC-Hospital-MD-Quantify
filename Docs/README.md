# Documentación General - QUANTIFY ![Microsoft Word](https://camo.githubusercontent.com/beb29946b4a70724ef7b9bcbccb3420a4c96905bdbb1d2f3c40941ade6156d67/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d6963726f736f66745f576f72642d3242353739413f7374796c653d666f722d7468652d6261646765266c6f676f3d6d6963726f736f66742d776f7264266c6f676f436f6c6f723d7768697465)

Bienvenido a la carpeta de documentación del ecosistema **Quantify**. Este directorio almacena todo el marco conceptual, técnico y operativo de la plataforma de ingeniería de bienestar y gamificación.

---

## 📂 Estructura de Documentación

A continuación se presenta la arquitectura de carpetas del repositorio, destacando de forma interactiva tu ubicación actual:

*   📂 **PC-Hospital-MD-Quantify/**
    *   📁 `DataBases/`
    *   📁 `DataModels/`
    *   📁 `Deliverables/`
    *   📂 **Docs/**  ◄── 🚀 **[ESTÁS EXPLORANDO ESTA CARPETA]**
        *   📁 `BRs/` *(Business Requirements)*
        *   📁 `FRs/` *(Functional Requirements)*
        *   📁 `GUIs/` *(Graphical User Interfaces)*
        *   📁 `NFRs/` *(Non-Functional Requirements)*
        *   📁 `UHs/` *(User Histories)*
        *   📁 `URs/` *(User Requirements)*

### 📋 Secciones Disponibles

*   **[BRs (Requerimientos de Negocio)](./BRs/README.md)**: Describe la visión, la justificación del negocio, los objetivos del sistema y las problemáticas abordadas.
*   **[FRs (Requerimientos Funcionales)](./FRs/README.md)**: Define detalladamente el comportamiento esperado de la plataforma y sus respectivos módulos operativos.
*   **[GUIs (Diseños de Interfaces)](./GUIs/README.md)**: Planificación y diseño de interfaces premium ("Engineering Aesthetic") para WebApp y WearableApp.
*   **[NFRs (Requerimientos No Funcionales)](./NFRs/README.md)**: Parámetros técnicos como escalabilidad híbrida, alto rendimiento (MongoDB), y tolerancias de volumen.
*   **[UHs (Historias de Usuario)](./UHs/README.md)**: Desglose de interacciones y escenarios de usuario estructurados.
*   **[URs (Requerimientos de Usuario)](./URs/README.md)**: Requisitos, expectativas de usabilidad y necesidades específicas del consumidor final.

---

## 👥 Equipo de Desarrollo

| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |

---

## ⚙️ Arquitectura del Sistema & Stack Tecnológico

Quantify implementa una arquitectura híbrida de base de datos con el fin de optimizar el rendimiento operativo y analítico:
1.  **MySQL**: Integridad transaccional y consistente para la gestión operativa de usuarios y configuraciones básicas.
2.  **MongoDB**: Registro, indexación y auditoría analítica de logs de alta frecuencia para el motor de gamificación y racha real.
3.  **Frontend**: React y Tailwind CSS, diseñado bajo la estética de ingeniería de precisión.
4.  **Backend**: Node.js con Express, orquestando lógica distribuida y poblamiento masivo (pruebas de estrés de hasta 300,000 registros).