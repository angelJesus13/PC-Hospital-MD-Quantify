# Requerimientos de Negocio (BRs) ![Microsoft Word](https://camo.githubusercontent.com/beb29946b4a70724ef7b9bcbccb3420a4c96905bdbb1d2f3c40941ade6156d67/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d6963726f736f66745f576f72642d3242353739413f7374796c653d666f722d7468652d6261646765266c6f676f3d6d6963726f736f66742d776f7264266c6f676f436f6c6f723d7768697465)

Esta sección contiene la especificación de los **Requerimientos de Negocio (Business Requirements - BRs)** para el proyecto **Quantify**. Estos requerimientos definen el "por qué" y los objetivos estratégicos de alto nivel que guían el diseño de la plataforma.

---

##  Estructura de Documentación

A continuación se presenta la arquitectura de carpetas del repositorio, destacando de forma interactiva tu ubicación actual:

*   📂 **PC-Hospital-MD-Quantify/**
    *   📁 `DataBases/`
    *   📁 `DataModels/`
    *   📁 `Deliverables/`
    *   📂 `Docs/`
        *   📂 **BRs/**  ◄── 
            *   📄 `.gitkeep`
            *   📄 **README.md**  ◄──
        *   📁 `FRs/`
        *   📁 `GUIs/`
        *   📁 `NFRs/`
        *   📁 `UHs/`
        *   📁 `URs/`

---

##  Objetivos de Negocio de Quantify

### 1. Eliminación de la "Inflación de Rachas"
Los rastreadores de hábitos actuales permiten que el usuario marque tareas de forma subjetiva e inexacta, devaluando el logro. **Quantify** soluciona esto requiriendo un **Motor de Gamificación de Precisión** con auditoría cruzada en bases de datos analíticas para validar las rachas de disciplina basadas en logs reales y verificables.

### 2. Escalabilidad Analítica y Operativa
Para asegurar la viabilidad comercial y técnica, la plataforma requiere una arquitectura de bases de datos híbrida:
*   **MySQL** garantiza la integridad operacional y de transacciones relacionales críticas (registro de usuarios, perfiles, etc.).
*   **MongoDB** permite el almacenamiento masivo y veloz de logs de comportamiento diarios y biometría a largo plazo para auditorías de salud.

### 3. Enganche y Retención Premium (Gamificación de Alta Fidelidad)
Fomentar la adopción persistente mediante un sistema dinámico de recompensas e insignias verificables, complementado con una experiencia de usuario (UX) sumamente refinada basada en el **"Engineering Aesthetic"**.

---

## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Completado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | En revisión |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En revisión |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | En revisión |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | En revisión |

