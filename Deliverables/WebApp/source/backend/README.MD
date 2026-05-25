# ➿Backend - Quantify

La carpeta `Deliverables/WebApp/Source/BackEnd` contiene el código fuente del backend del sistema web **Quantify**. Este módulo es responsable de gestionar la lógica del servidor, el procesamiento de información, la autenticación de usuarios y la comunicación con la base de datos.

---
<p>
  <img src="https://img.shields.io/badge/Backend-FF6B6B?style=for-the-badge&logo=nodedotjs&logoColor=white" /> 
  <img align="right" src="https://img.shields.io/badge/WebApp-4CAF50?style=for-the-badge&logo=react&logoColor=white" />
</p>

# 📖 Descripción General

El backend representa la capa servidora principal del sistema y permite la comunicación entre el frontend, la base de datos y los distintos servicios internos de la plataforma.

Su función principal es:

- Procesar solicitudes HTTP.
- Administrar información del sistema.
- Controlar la autenticación y seguridad.
- Gestionar la comunicación en tiempo real.
- Mantener organizada la lógica del negocio.

Además, su arquitectura modular facilita el mantenimiento, escalabilidad y futuras mejoras del proyecto.

---

# ⚙️ Funcionalidades Principales

Dentro de este módulo se implementan las siguientes funcionalidades:

- Gestión de API y endpoints.
- Procesamiento de solicitudes del cliente.
- Controladores y lógica de negocio.
- Administración de usuarios.
- Sistema de autenticación y validación.
- Modelos y esquemas de datos.
- Conexión y manejo de base de datos.
- Configuración general del servidor.
- Gestión de dependencias y paquetes.
- Comunicación en tiempo real mediante Socket.IO.
- Organización modular del proyecto.

---

# 🚀 Tecnologías Utilizadas

El backend fue desarrollado utilizando las siguientes tecnologías:

| Tecnología | Descripción |
|---|---|
| Node.js | Entorno de ejecución para JavaScript |
| Express.js | Framework para el servidor |
| MongoDB | Base de datos NoSQL |
| Mongoose | Modelado de datos para MongoDB |
| Socket.IO | Comunicación en tiempo real |
| JWT | Autenticación y seguridad |
| Nodemon | Monitoreo automático en desarrollo |

---

# 🎯 Objetivo del Backend

El objetivo principal del backend es proporcionar una infraestructura segura, eficiente y escalable que permita:

- Centralizar la administración de información.
- Facilitar la comunicación con el frontend.
- Proteger el acceso a los datos.
- Optimizar el rendimiento del sistema.
- Mantener estabilidad y escalabilidad.

---

# 📂 Estructura de Carpetas

|- Databases
|- DataModels
|- Deliverables
|  |- API
|  |- WearableApp
|  |- WebApp
|  |  |- DeployManual
|  |  |- Source
|  |  |  |- FrontEnd
|  |  |  |- **BackEnd**
|  |  |- UserManual
|- Docs

---

# 🛠️ Organización del Backend

El backend se encuentra estructurado en distintos módulos para facilitar su administración:

| Carpeta | Función |
|---|---|
| Databases | Configuración y conexión de bases de datos |
| DataModels | Modelos y esquemas de información |
| Controllers | Lógica de negocio y controladores |
| Routes | Definición de endpoints y rutas |
| Middlewares | Validaciones y seguridad |
| Config | Variables y configuraciones generales |

---

# 🔐 Seguridad

El sistema implementa distintos mecanismos de seguridad para proteger la información:

- Validación de datos.
- Autenticación mediante JWT.
- Protección de rutas privadas.
- Manejo seguro de sesiones.
- Control de acceso a recursos.

---

# 📡 Comunicación en Tiempo Real

El backend utiliza **Socket.IO** para permitir:

- Actualizaciones en tiempo real.
- Comunicación instantánea entre clientes.
- Sincronización de información.
- Eventos dinámicos dentro de la plataforma.

---

# 📌 Importancia del Backend

El backend es uno de los componentes fundamentales de **Quantify**, ya que permite administrar toda la lógica interna del sistema y garantizar una comunicación eficiente entre los distintos módulos de la plataforma.

Gracias a su arquitectura modular y escalable, el sistema puede mantenerse organizado, seguro y preparado para futuras actualizaciones.
## Equipo de Desarrollo

| Colaborador | Rol | Github | Estado |
| :--- | :--- | :--- | :--- |
| **Angel de Jesús** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) | Revisado y Aprobado |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) | En Revision |
| **Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) | En Revision |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) | Completado |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) | Completado |

