# PC-Hospital-MD (Medical Register & Remote Monitoring)

<p align="center">
  <img src="./assets/logo.jpg" alt="Hospital MD Logo" width="220" style="border-radius: 8px;" />
</p>

<div align="center">
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Architecture-Hybrid_SQL_NoSQL-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Version-1.1.0-orange?style=for-the-badge" />
</div>

---

### DESCRIPCIÓN Y PROPÓSITO DEL SISTEMA (Criterio 01)

**PC-Hospital-MD** es una plataforma integral de Registros Médicos (EHR) y monitoreo remoto de pacientes ambulatorios. Diseñado por el **Equipo Quantify**, su propósito es proveer a los profesionales de la salud un Dashboard en tiempo real que reciba y procese signos vitales mediante una arquitectura híbrida de alta disponibilidad.

#### Dependencias de Subsistemas Externos y Autonomía
Para garantizar el funcionamiento **autónomo**, el núcleo de la aplicación (Gestión de expedientes y Autenticación) no depende de servicios de terceros. Sin embargo, se delimitan las siguientes integraciones externas:
1.  **Wearables API (Terceros):** Los sensores físicos (relojes) emiten POSTs a nuestra API. Si el wearable pierde conexión, nuestro sistema opera autónomamente con los datos cacheados.
2.  **Notificaciones SMS/Email (Opcional):** Dependencia de Twilio/SendGrid para alertas críticas fuera de la plataforma web.

### STACK TECNOLÓGICO

| Capa               | Tecnologías                                                                                                                                                                                                             |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend**       | ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) |
| **Backend**        | ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white) ![Express](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)  |
| **Bases de Datos** | ![MySQL](https://img.shields.io/badge/MySQL-00000f?style=for-the-badge&logo=mysql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)             |

---

### GUÍA DE INSTALACIÓN Y CONFIGURACIÓN (Criterio 02)

Para desplegar localmente el entorno de desarrollo, asegúrese de cumplir estrictamente este orden:

**1. Requisitos Previos (Versiones)**
*   Node.js (v18.17.0 LTS o superior).
*   MySQL (v8.0+) ejecutándose en el puerto `3306`.
*   MongoDB (v6.0+) ejecutándose localmente en el puerto `27017` o un clúster de Atlas.
*   Git para clonar el repositorio.

**2. Clonación e Instalación de Dependencias**
```bash
git clone https://github.com/angelJesus13/PC-Hospital-MD-Quantify.git
cd PC-Hospital-MD-Quantify
# Instalar dependencias del backend y frontend
cd Deliverables/API && npm install
cd ../WebApp/Source/FrontEnd && npm install
```

**3. Archivos de Entorno (.env.example)**
Dentro de la carpeta `API/`, copie el archivo de ejemplo y configure sus variables locales:
```bash
cp .env.example .env
```
*Contenido clave del `.env`:*
```env
PORT=3000
DB_HOST=127.0.0.1
DB_USER=root
DB_PASS=Secreta123
DB_NAME=hospital_db
MONGO_URI=mongodb://localhost:27017/biometrics
JWT_SECRET=su_clave_segura_rs256
```

**4. Orden de Arranque de los Subsistemas**
1.  Inicie los motores de bases de datos (MySQL y MongoDB).
2.  Levante la API Backend: `cd Deliverables/API && npm run dev`.
3.  Levante el Dashboard Frontend: `cd Deliverables/WebApp/Source/FrontEnd && npm start`.

---

### GUÍA DE PRUEBAS Y TESTING (Criterio 03)

El ecosistema cuenta con pruebas automatizadas (Jest/Supertest) diseñadas para ejecutarse tanto en aislamiento como en integración total.

**1. Pruebas Autónomas (Unitarias con Mocks)**
Para ejecutar las pruebas sin necesidad de levantar bases de datos externas (MySQL/MongoDB), el sistema provee *stubs* preconfigurados para las capas de persistencia.
*   **Comando:** `npm run test:unit`
*   **Alcance:** Evalúa la lógica de los controladores, el motor de alertas y validaciones JWT inyectando dependencias falsas (mocks).

**2. Pruebas de Integración y Estrés (Dependencias Externas)**
Estas pruebas requieren los motores de bases de datos activos, simulando ráfagas masivas desde los wearables.
*   **Comando:** `npm run test:integration`
*   **Alcance:** Prueba de carga insertando 300,000 registros biométricos (`wearable_logs`) en MongoDB mediante la librería `Artillery`.

---

### CONTRIBUCIÓN AL PROYECTO
Las reglas para realizar Commits, Pull Requests (PRs) y las convenciones de Linting requeridas para todo el equipo multidisciplinario se detallan estrictamente en el documento 📄 **[CONTRIBUTING.md](./CONTRIBUTING.md)** (Criterio 20).

---

## Equipo de Desarrollo (Equipo Quantify)

| Colaborador | Rol | Github |
| :--- | :--- | :--- |
| **Angel de Jesús Baños Téllez** | Tech Lead & Architecture | [@angelJesus13](https://github.com/angelJesus13) |
| **Francisco Garcia G** | Lead Backend Developer | [@F-Anks](https://github.com/F-Anks) |
| **Al Farias Leyva** | Frontend & Documentation | [@farias](https://github.com/farias) |
| **Artiaga Morales** | QA & Data Science | [@artiaga](https://github.com/artiaga) |
| **Brian Jesús Mendoza Márquez** | Fullstack Developer | [@BrianMendoza](https://github.com/BrianMendoza) |
